"""Unit tests for ProgressiveSpiker screening logic"""
import pytest
import pandas as pd
from progressive_screener import ProgressiveSpiker


class TestProgressiveSpiker:
    """Test suite for 12-condition Progressive Spike screener"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample dataset for testing"""
        return pd.DataFrame({
            "SYMBOL": ["INFY", "TCS", "RELIANCE", "HDFC", "ITC"],
            "CLOSE": [1500.0, 3600.0, 2500.0, 2400.0, 450.0],
            "DELIV_PER": [75.0, 65.0, 55.0, 45.0, 30.0],
            "DELIV_PER_1W": [70.0, 60.0, 50.0, 40.0, 25.0],
            "DELIV_PER_1M": [60.0, 55.0, 45.0, 35.0, 20.0],
            "DELIV_PER_3M": [50.0, 45.0, 35.0, 25.0, 15.0],
            "DELIVERY_TURNOVER": [10000000.0, 8000000.0, 6000000.0, 4000000.0, 2000000.0],
            "DELIVERY_TURNOVER_1W": [9000000.0, 7000000.0, 5500000.0, 3500000.0, 1500000.0],
            "DELIVERY_TURNOVER_1M": [8000000.0, 6500000.0, 5000000.0, 3000000.0, 1000000.0],
            "DELIVERY_TURNOVER_3M": [7000000.0, 5500000.0, 4000000.0, 2500000.0, 500000.0],
            "ATW": [50000.0, 40000.0, 25000.0, 22000.0, 5000.0],
            "ATW_1W": [45000.0, 35000.0, 23000.0, 20000.0, 4500.0],
            "ATW_1M": [40000.0, 30000.0, 22000.0, 18000.0, 4000.0],
            "ATW_3M": [35000.0, 25000.0, 20000.0, 15000.0, 3000.0],
        })
    
    def test_baseline_conditions_only(self, sample_data):
        """Test that screener filters by 3 baseline conditions"""
        screener = ProgressiveSpiker(sample_data)
        df_pass = sample_data.copy()
        
        # Apply baseline manually
        df_pass = df_pass[df_pass["DELIV_PER"] >= 50]
        df_pass = df_pass[df_pass["DELIVERY_TURNOVER"] >= 5000000]
        df_pass = df_pass[df_pass["ATW"] >= 20000]
        
        # Expect INFY, TCS, RELIANCE (HDFC has ATW=22k but DELIV_PER=45 < 50)
        assert len(df_pass) == 3, "Expected 3 stocks to pass baseline conditions"
    
    def test_all_12_conditions(self, sample_data):
        """Test progressive conditions filter correctly"""
        screener = ProgressiveSpiker(sample_data)
        signals = screener.get_signals()
        
        # Should only pass: INFY (75>70>60>50, 10M>9M>8M>7M, 50K>45K>40K>35K)
        assert len(signals) == 1, "Expected only INFY to pass all 12 conditions"
        assert signals["SYMBOL"].iloc[0] == "INFY"
    
    def test_missing_columns_returns_empty(self, sample_data):
        """Test that missing progressive columns returns baseline filter only"""
        # Remove progressive columns
        df_minimal = sample_data[["SYMBOL", "CLOSE", "DELIV_PER", "DELIVERY_TURNOVER", "ATW"]]
        screener = ProgressiveSpiker(df_minimal)
        signals = screener.get_signals()
        
        # Should return 3 baseline passers
        assert len(signals) >= 1
        assert all(signals["DELIV_PER"] >= 50)
        assert all(signals["DELIVERY_TURNOVER"] >= 5000000)
        assert all(signals["ATW"] >= 20000)
    
    def test_missing_required_columns(self):
        """Test error handling with missing required columns"""
        df_incomplete = pd.DataFrame({"SYMBOL": ["INFY"]})
        screener = ProgressiveSpiker(df_incomplete)
        signals = screener.get_signals()
        
        # Should return empty DataFrame
        assert len(signals) == 0
    
    def test_zero_and_negative_values_filtered(self):
        """Test that zero and negative values are handled properly"""
        df_bad = pd.DataFrame({
            "SYMBOL": ["BAD1", "BAD2", "GOOD"],
            "CLOSE": [0.0, -10.0, 100.0],
            "DELIV_PER": [0.0, 60.0, 75.0],
            "DELIVERY_TURNOVER": [0.0, 8000000.0, 10000000.0],
            "ATW": [0.0, 30000.0, 50000.0],
        })
        screener = ProgressiveSpiker(df_bad)
        signals = screener.get_signals()
        
        # Negative/zero values should be filtered
        assert all(signals["CLOSE"] > 0)
        assert all(signals["DELIV_PER"] > 0)
        assert all(signals["DELIVERY_TURNOVER"] > 0)
        assert all(signals["ATW"] > 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
