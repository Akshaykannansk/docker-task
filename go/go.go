package main
import (
	"database/sql"
	"fmt"	
	_"github.com/lib/pq"
	// "github.com/jasonlvhit/gocron"
	"time"

)


const (
	host     = "localhost"
	port     = 5432
	user     = "postgres"
	password = "psql"
	dbname   = "django1"
)
 
func main() { 

	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+"password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	CheckError(err)
	defer db.Close()
	// gocron.Every(1).Second().Do(sponsor_bonus_calculation, db)
	// gocron.Every(1).Second().Do(badge, db)
	// gocron.Every(1).Second().Do(bonus, db)
	// gocron.Every(1).Second().Do(couponexpirations ,db)
	// <-gocron.Start()		
	// badge(db)
	// bonus(db)
	couponexpirations(db)

	
}

func CheckError(err error) {
	if err != nil {
		panic(err)
		
	}
}


func badge(db *sql.DB){
	// Prepare the SQL statement to retrieve user IDs
	stmt, err := db.Prepare("SELECT id FROM authentication_customuser")
	CheckError(err)
	defer stmt.Close()

	// Execute the SQL statement
	rows, err := stmt.Query()
	CheckError(err)
	defer rows.Close()

	// Loop through the rows of the result set and print the user IDs
	var id int
	for rows.Next() {
		if err := rows.Scan(&id); err != nil {
			panic(err)
		}
		// fmt.Println(id)

		// Query the total for the current user ID
		totalQuery := "SELECT total FROM shop_orders WHERE user_id = $1"
		totalRows, err := db.Query(totalQuery, id)
		CheckError(err)
		defer totalRows.Close()

		
		var order float64
		var sum float64
		for totalRows.Next() {
			if err := totalRows.Scan(&order); err != nil {
				panic(err)
			}
			sum += order
		}

		b := ""
		if sum > 500 && sum < 1000 {
			b = "Bronze" 
		}else if sum >=1000 && sum < 2000 {
			b = "Silver"
		} else if sum >=2000 && sum < 5000 {
			b = "Gold"
		} else if sum >= 5000 && sum < 10000{
			b = "Diamond"
		} else if sum >= 10000{
			b = "Platinum"
		}else {
			b = "lol"
		}

		// dynamic
		
		updateDynStmt := `update "shop_bonuses" set "order_total" = $1, "badge" = $2 where "user_id" = $3`
		_, e := db.Exec(updateDynStmt, sum, b, id)
		CheckError(e)
		
		
		fmt.Println("go runing...  : checking badges" )
		

	}

}
func bonus(db *sql.DB){
	totalQuery := "SELECT total ,user_id ,id FROM shop_orders WHERE calculation = 0 and user_id != '1'"
	totalRows, err := db.Query(totalQuery)
	CheckError(err)
	defer totalRows.Close()

	var sum float64
	var id int
	var oid int
	for totalRows.Next() {
		if err := totalRows.Scan(&sum ,&id,&oid); err != nil {
			panic(err)
		}
		fmt.Println("sum : ",sum,"   ","id :", id , "oid : ",oid)
	
		sponsor_bonus_calculation(sum,id,db)

		updateDynStmt := `update "shop_orders" set "calculation" = 1 where "id" = $1`
		_, e := db.Exec(updateDynStmt,oid)
		CheckError(e)

	}	   

}

func sponsor_bonus_calculation(sum float64,id int ,db *sql.DB) {
	


	query := "SELECT id FROM authentication_customuser WHERE username = (SELECT sponsorname FROM authentication_customuser WHERE id = $1)"
	row := db.QueryRow(query, id)

	var sponsorID int
	if err := row.Scan(&sponsorID); err != nil {
		panic(err)
	}

	fmt.Println("sponsor id  ",sponsorID)


	badgequery := "SELECT badge FROM shop_bonuses WHERE user_id = $1"
	badgerow := db.QueryRow(badgequery,sponsorID)
	var badge string
	if err := badgerow.Scan(&badge); err != nil {
		panic(err)
	}

	fmt.Println("sponsorbadge  :",badge)
	Sponsor_Bonus := 0.00
	if badge == "Bronze" {
		Bronzerow := db.QueryRow("SELECT percentage FROM home_bonusconfig WHERE id = 1")

		if err := Bronzerow.Scan(&Sponsor_Bonus); err != nil {
			panic(err)
		}
    }else if badge == "Silver" {
		Silverrow := db.QueryRow("SELECT percentage FROM home_bonusconfig WHERE id = 1")

		if err := Silverrow.Scan(&Sponsor_Bonus); err != nil {
			panic(err)
		}
	}else if badge == "Gold" {   
		Goldrow := db.QueryRow("SELECT percentage FROM home_bonusconfig WHERE id = 1")

		if err := Goldrow.Scan(&Sponsor_Bonus); err != nil {
			panic(err)
		}		
    }else if badge == "Diamond" {

		Diamondrow := db.QueryRow("SELECT percentage FROM home_bonusconfig WHERE id = 1")

		if err := Diamondrow.Scan(&Sponsor_Bonus); err != nil {
			panic(err)
		}		
	}else if badge == "Platinum"{
		Platinumrow := db.QueryRow("SELECT percentage FROM home_bonusconfig WHERE id = 1")
	
		if err := Platinumrow.Scan(&Sponsor_Bonus); err != nil {
			panic(err)
		}	
	}else{
		Sponsor_Bonus =0.00
	}




	walletQuery := "SELECT balance FROM wallet_userwallet WHERE id = $1"
	walletrow := db.QueryRow(walletQuery, sponsorID)
	var wallet float64
	if err := walletrow.Scan(&wallet); err != nil {
		panic(err)
	}
	bonus := sum*Sponsor_Bonus/100
	wallet += bonus
	fmt.Println("wallet =",wallet)
	


	updateDynStmt := `update "wallet_userwallet" set "balance" = $1 where "user_id" = $2`
	_, e := db.Exec(updateDynStmt, wallet, sponsorID)
	CheckError(e)


	insertStmt := `INSERT INTO "home_bonushistory" ("user_id", "bonusesamount" ,"sponsor_id","created_at") VALUES ($1, $2,$3,$4)`
	_, ex := db.Exec(insertStmt, id, bonus ,sponsorID,time.Now())
	CheckError(ex)
	


	SwalletQuery := "SELECT balance FROM wallet_userwallet WHERE id = 1"
	Swalletrow := db.QueryRow(SwalletQuery)
	var Swallet float64
	if err := Swalletrow.Scan(&Swallet); err != nil {
		panic(err)
	}
	Swallet -= bonus
	fmt.Println("wallet =",Swallet)

	SupdateDynStmt := `update "wallet_userwallet" set "balance" = $1 where "user_id" = 1`
	_, er := db.Exec(SupdateDynStmt, Swallet)
	CheckError(er)
	fmt.Println("go runing...  : sponsor_bonus_calculation" )


}




func couponexpirations(db *sql.DB) {


	_, er := db.Exec(`UPDATE "wallet_coupon" SET "is_expired" = TRUE WHERE "expiration_date" < $1`, time.Now())
	CheckError(er)


	transferred,err := db.Query("SELECT discount_amount, id ,user_id FROM wallet_coupon WHERE is_expired = TRUE")
	CheckError(err)
	defer transferred.Close()
	var coupon_amount float64
	var id int
	var user_id int
	for transferred.Next() {
		if err := transferred.Scan(&coupon_amount,&id,&user_id); err != nil {

			panic(err)
		}
	
		if coupon_amount > 0 {
	
			walletQuery := "SELECT balance FROM wallet_userwallet WHERE user_id = $1"
			walletrow := db.QueryRow(walletQuery,user_id)
			var wallet float64
			if err := walletrow.Scan(&wallet); err != nil {
				panic(err)
			}
			wallet += coupon_amount
			fmt.Println("wallet =",wallet)
	
			_, er := db.Exec(`UPDATE "wallet_userwallet" SET "balance" = $1  WHERE user_id = $2`, wallet,user_id)
			CheckError(er)
	
			_, err := db.Exec(`UPDATE "wallet_coupon" SET "discount_amount" = 0 WHERE id = $1`,id)
			CheckError(err)
	
			fmt.Println("go runing...  : checking couponexpirations" )
	
	
	
		}

	}	   

	

	
}





