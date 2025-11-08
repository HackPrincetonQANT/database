USE ROLE BALANCEIQ_ROLE;
USE WAREHOUSE BALANCEIQ_WH;
USE DATABASE BALANCEIQ_DB;
USE SCHEMA CORE;

-- Users and profile (personalization knobs)
CREATE OR REPLACE TABLE users (
  user_id            STRING PRIMARY KEY,
  phone_e164         STRING,
  email              STRING,
  created_at         TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE user_profile (
  user_id            STRING PRIMARY KEY,
  display_name       STRING,
  age                NUMBER(3,0),
  location_country   STRING,
  location_region    STRING,
  tz                 STRING DEFAULT 'America/New_York',
  income_bracket     STRING,        -- 'low'|'mid'|'high' (optional)
  budgeting_style    STRING,        -- 'strict'|'moderate'|'loose'
  saving_goals_json  VARIANT,       -- [{goal_id,title,target_amount,saved_amount}, ...]
  preferences_json   VARIANT,       -- {"coffee_policy":"always_want", ...}
  updated_at         TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
  CONSTRAINT fk_user_prof FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Global taxonomy with meaningful defaults
CREATE OR REPLACE TABLE category_taxonomy (
  category           STRING,
  subcategory        STRING,
  default_needwant   STRING,          -- 'need'|'want'
  priority           NUMBER(2,0) DEFAULT 5,  -- lower = more essential
  notes              STRING,
  PRIMARY KEY (category, subcategory)
);

-- User overrides (win over taxonomy)
CREATE OR REPLACE TABLE user_category_rules (
  user_id            STRING,
 