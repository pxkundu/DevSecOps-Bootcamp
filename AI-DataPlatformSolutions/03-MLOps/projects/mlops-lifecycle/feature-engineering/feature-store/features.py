"""
Feature Definitions for MLOps Platform

This module defines features for various ML models including customer churn prediction,
recommendation engine, and fraud detection.
"""

from datetime import timedelta
from feast import (
    Entity,
    Feature,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    RequestSource,
    ValueType,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int32, Int64, String, Bool, UnixTimestamp
import pandas as pd


# ============================================================================
# ENTITIES
# ============================================================================

# Customer entity for customer-related features
customer = Entity(
    name="customer_id",
    description="Customer identifier",
    value_type=ValueType.STRING,
)

# Product entity for product-related features
product = Entity(
    name="product_id", 
    description="Product identifier",
    value_type=ValueType.STRING,
)

# Transaction entity for transaction-related features
transaction = Entity(
    name="transaction_id",
    description="Transaction identifier", 
    value_type=ValueType.STRING,
)


# ============================================================================
# DATA SOURCES
# ============================================================================

# Customer demographic data source
customer_demographics_source = FileSource(
    name="customer_demographics",
    path="/feast/data/customer_demographics.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Customer behavior data source
customer_behavior_source = FileSource(
    name="customer_behavior",
    path="/feast/data/customer_behavior.parquet", 
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Product catalog data source
product_catalog_source = FileSource(
    name="product_catalog",
    path="/feast/data/product_catalog.parquet",
    timestamp_field="event_timestamp", 
    created_timestamp_column="created_timestamp",
)

# Transaction data source
transaction_source = FileSource(
    name="transactions",
    path="/feast/data/transactions.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp", 
)

# Real-time customer events (push source)
customer_events_source = PushSource(
    name="customer_events",
    batch_source=customer_behavior_source,
)


# ============================================================================
# FEATURE VIEWS - Customer Demographics
# ============================================================================

customer_demographics_fv = FeatureView(
    name="customer_demographics",
    entities=[customer],
    ttl=timedelta(days=365),  # Customer data changes infrequently
    schema=[
        Field(name="age", dtype=Int32),
        Field(name="gender", dtype=String),
        Field(name="income_level", dtype=String),
        Field(name="education_level", dtype=String),
        Field(name="marital_status", dtype=String),
        Field(name="num_dependents", dtype=Int32),
        Field(name="employment_status", dtype=String),
        Field(name="city", dtype=String),
        Field(name="state", dtype=String),
        Field(name="country", dtype=String),
        Field(name="customer_since_days", dtype=Int32),
        Field(name="preferred_contact_method", dtype=String),
    ],
    source=customer_demographics_source,
    tags={"team": "customer_analytics", "type": "batch"},
)


# ============================================================================
# FEATURE VIEWS - Customer Behavior & Engagement
# ============================================================================

customer_behavior_fv = FeatureView(
    name="customer_behavior",
    entities=[customer],
    ttl=timedelta(days=7),  # Behavior data is more recent
    schema=[
        # Transaction patterns
        Field(name="total_transactions_30d", dtype=Int32),
        Field(name="total_amount_30d", dtype=Float64),
        Field(name="avg_transaction_amount_30d", dtype=Float64),
        Field(name="max_transaction_amount_30d", dtype=Float64),
        Field(name="days_since_last_transaction", dtype=Int32),
        
        # Product preferences
        Field(name="favorite_category", dtype=String),
        Field(name="num_categories_purchased_30d", dtype=Int32),
        Field(name="repeat_purchase_rate_30d", dtype=Float32),
        
        # Engagement metrics
        Field(name="website_visits_30d", dtype=Int32),
        Field(name="total_session_duration_30d", dtype=Float32),
        Field(name="avg_session_duration_30d", dtype=Float32),
        Field(name="pages_per_session_30d", dtype=Float32),
        Field(name="email_opens_30d", dtype=Int32),
        Field(name="email_clicks_30d", dtype=Int32),
        
        # Support interactions
        Field(name="support_tickets_30d", dtype=Int32),
        Field(name="support_satisfaction_score", dtype=Float32),
        
        # Loyalty indicators
        Field(name="loyalty_program_member", dtype=Bool),
        Field(name="loyalty_points_balance", dtype=Int32),
        Field(name="referrals_made_30d", dtype=Int32),
    ],
    source=customer_behavior_source,
    tags={"team": "customer_analytics", "type": "batch"},
)


# ============================================================================
# FEATURE VIEWS - Product Catalog & Performance
# ============================================================================

product_features_fv = FeatureView(
    name="product_features",
    entities=[product],
    ttl=timedelta(days=30),  # Product data updates monthly
    schema=[
        # Basic product info
        Field(name="category", dtype=String),
        Field(name="subcategory", dtype=String),
        Field(name="brand", dtype=String),
        Field(name="price", dtype=Float64),
        Field(name="discount_percentage", dtype=Float32),
        Field(name="is_seasonal", dtype=Bool),
        Field(name="launch_date_days_ago", dtype=Int32),
        
        # Performance metrics
        Field(name="avg_rating", dtype=Float32),
        Field(name="num_reviews", dtype=Int32),
        Field(name="sales_rank_in_category", dtype=Int32),
        Field(name="inventory_level", dtype=Int32),
        Field(name="reorder_point", dtype=Int32),
        
        # Sales performance
        Field(name="units_sold_30d", dtype=Int32),
        Field(name="revenue_30d", dtype=Float64),
        Field(name="conversion_rate_30d", dtype=Float32),
        Field(name="return_rate_30d", dtype=Float32),
        Field(name="view_to_purchase_rate_30d", dtype=Float32),
    ],
    source=product_catalog_source,
    tags={"team": "product_analytics", "type": "batch"},
)


# ============================================================================
# FEATURE VIEWS - Transaction & Payment Features
# ============================================================================

transaction_features_fv = FeatureView(
    name="transaction_features", 
    entities=[transaction],
    ttl=timedelta(days=90),  # Transaction data for fraud detection
    schema=[
        # Transaction details
        Field(name="amount", dtype=Float64),
        Field(name="currency", dtype=String),
        Field(name="payment_method", dtype=String),
        Field(name="merchant_category", dtype=String),
        Field(name="transaction_hour", dtype=Int32),
        Field(name="transaction_day_of_week", dtype=Int32),
        Field(name="is_weekend", dtype=Bool),
        
        # Location and device
        Field(name="city", dtype=String),
        Field(name="country", dtype=String),
        Field(name="device_type", dtype=String),
        Field(name="ip_country", dtype=String),
        Field(name="is_mobile", dtype=Bool),
        
        # Risk indicators
        Field(name="is_high_risk_merchant", dtype=Bool),
        Field(name="velocity_1h", dtype=Int32),
        Field(name="velocity_24h", dtype=Int32),
        Field(name="amount_deviation_from_avg", dtype=Float32),
        Field(name="is_first_time_merchant", dtype=Bool),
        Field(name="days_since_last_transaction", dtype=Int32),
    ],
    source=transaction_source,
    tags={"team": "fraud_detection", "type": "batch"},
)


# ============================================================================
# REAL-TIME FEATURE VIEWS
# ============================================================================

# Real-time customer events for immediate fraud detection
customer_events_fv = FeatureView(
    name="customer_events_realtime",
    entities=[customer],
    ttl=timedelta(hours=1),  # Very fresh data for real-time decisions
    schema=[
        Field(name="current_session_duration", dtype=Float32),
        Field(name="pages_viewed_current_session", dtype=Int32),
        Field(name="current_cart_value", dtype=Float64),
        Field(name="current_cart_items", dtype=Int32),
        Field(name="time_on_current_page", dtype=Float32),
        Field(name="clicks_per_minute", dtype=Float32),
        Field(name="is_peak_hours", dtype=Bool),
        Field(name="concurrent_sessions", dtype=Int32),
    ],
    source=customer_events_source,
    tags={"team": "real_time_analytics", "type": "streaming"},
)


# ============================================================================
# ON-DEMAND FEATURE VIEWS (Computed Features)
# ============================================================================

# Request-time features for churn prediction
@on_demand_feature_view(
    sources=[
        customer_demographics_fv,
        customer_behavior_fv,
    ],
    schema=[
        Field(name="clv_score", dtype=Float32),
        Field(name="engagement_score", dtype=Float32), 
        Field(name="churn_risk_score", dtype=Float32),
        Field(name="value_segment", dtype=String),
    ],
)
def customer_derived_features(inputs: pd.DataFrame) -> pd.DataFrame:
    """Compute derived customer features for churn prediction."""
    df = pd.DataFrame()
    
    # Customer Lifetime Value Score
    df["clv_score"] = (
        inputs["total_amount_30d"] * 12 * 
        (inputs["customer_since_days"] / 365) * 
        (1 + inputs["repeat_purchase_rate_30d"])
    ).fillna(0)
    
    # Engagement Score (0-100)
    df["engagement_score"] = (
        (inputs["website_visits_30d"] * 2) +
        (inputs["email_opens_30d"] * 1) + 
        (inputs["email_clicks_30d"] * 3) +
        (inputs["total_transactions_30d"] * 5)
    ).clip(0, 100)
    
    # Churn Risk Score (0-1, higher = more likely to churn)
    df["churn_risk_score"] = (
        (inputs["days_since_last_transaction"] / 90) * 0.4 +
        ((30 - inputs["website_visits_30d"]) / 30) * 0.3 +
        ((5 - inputs["total_transactions_30d"]) / 5) * 0.3
    ).clip(0, 1)
    
    # Value Segment
    df["value_segment"] = pd.cut(
        df["clv_score"],
        bins=[0, 1000, 5000, 15000, float('inf')],
        labels=["Low", "Medium", "High", "VIP"]
    ).astype(str)
    
    return df


# Product recommendation features
@on_demand_feature_view(
    sources=[
        product_features_fv,
        customer_behavior_fv,
    ],
    schema=[
        Field(name="popularity_score", dtype=Float32),
        Field(name="personalization_score", dtype=Float32),
        Field(name="price_attractiveness", dtype=Float32),
        Field(name="recommendation_score", dtype=Float32),
    ],
)
def recommendation_features(inputs: pd.DataFrame) -> pd.DataFrame:
    """Compute features for product recommendations."""
    df = pd.DataFrame()
    
    # Popularity score based on sales and ratings
    df["popularity_score"] = (
        inputs["units_sold_30d"] * 0.6 + 
        inputs["avg_rating"] * inputs["num_reviews"] * 0.4
    ).fillna(0)
    
    # Personalization score (category match with customer preference)
    df["personalization_score"] = (
        inputs["category"] == inputs["favorite_category"]
    ).astype(float)
    
    # Price attractiveness (discount and price relative to category average)
    df["price_attractiveness"] = (
        inputs["discount_percentage"] * 0.7 +
        (1 - inputs["price"] / inputs["price"].max()) * 0.3
    ).fillna(0)
    
    # Overall recommendation score
    df["recommendation_score"] = (
        df["popularity_score"] * 0.3 +
        df["personalization_score"] * 0.4 +
        df["price_attractiveness"] * 0.3
    )
    
    return df


# Fraud detection features
@on_demand_feature_view(
    sources=[
        transaction_features_fv,
        customer_behavior_fv,
    ],
    schema=[
        Field(name="velocity_risk_score", dtype=Float32),
        Field(name="amount_risk_score", dtype=Float32),
        Field(name="location_risk_score", dtype=Float32),
        Field(name="overall_fraud_score", dtype=Float32),
    ],
)
def fraud_detection_features(inputs: pd.DataFrame) -> pd.DataFrame:
    """Compute fraud detection features."""
    df = pd.DataFrame()
    
    # Velocity risk (high frequency transactions)
    df["velocity_risk_score"] = (
        inputs["velocity_1h"] * 0.6 + inputs["velocity_24h"] * 0.4
    ).fillna(0) / 10  # Normalize
    
    # Amount risk (deviation from normal spending)
    df["amount_risk_score"] = inputs["amount_deviation_from_avg"].abs().fillna(0)
    
    # Location risk (new locations, high-risk countries)
    df["location_risk_score"] = (
        inputs["is_high_risk_merchant"].astype(float) * 0.5 +
        inputs["is_first_time_merchant"].astype(float) * 0.3 +
        (inputs["ip_country"] != inputs["country"]).astype(float) * 0.2
    ).fillna(0)
    
    # Overall fraud score
    df["overall_fraud_score"] = (
        df["velocity_risk_score"] * 0.4 +
        df["amount_risk_score"] * 0.3 +
        df["location_risk_score"] * 0.3
    ).clip(0, 1)
    
    return df
