#!/usr/bin/env bash

# Database for Messages
export DATABASE_URL = 'sqlite:///chat.db'

# Database for Main Database (TopMarket, BuySell)
export PROD_PG_USER = 'market_user'
export PROD_PG_PASSWORD = 'pass12pass'
export PROD_PG_HOST = 'localhost'
export PROD_PG_PORT = '5432'
export PROD_PG_NAME = 'market_dev'

# Redis for caching
export REDIS_HOST='localhost'
export REDIS_PORT='6379'
