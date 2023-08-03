CREATE TABLE 
	users( user_id UUID NOT NULL PRIMARY KEY, 
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	gender VARCHAR(8) NOT NULL CHECK (gender = 'Male' OR gender = 'Female'),
	date_of_birth DATE NOT NULL,
	phone_number VARCHAR(12) NOT NULL,
	phone_type VARCHAR(6) NOT NULL,
	ssn VARCHAR(11) NOT NULL,
	email VARCHAR(150) NOT NULL,
	account_creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	account_status VARCHAR(8) DEFAULT 'active',
	UNIQUE(ssn),
	UNIQUE(email),
	UNIQUE(phone_number)
	);

CREATE TABLE
	checking_accounts (checking_id UUID NOT NULL PRIMARY KEY,
	account_number INT NOT NULL,
	account_status VARCHAR(6) NOT NULL,
	overdraft_limit INT,
	last_transaction DATE,
	UNIQUE(account_number),
	user_id UUID,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
	);


CREATE TABLE
	checking_details (checking_details_id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
	user_id UUID,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	checking_account_id UUID,
	FOREIGN KEY (checking_account_id) REFERENCES checking_accounts(checking_id),
	account_number INT NOT NULL,
	transaction_amount INT,
	transaction_type VARCHAR(8),
	transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
	account_balance INT NOT NULL DEFAULT 0,
	memo VARCHAR(150)
	)