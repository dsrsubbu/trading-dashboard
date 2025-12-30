"""Unit tests for configuration module"""
import pytest
import os
import logging
from config import Config


class TestConfig:
    """Test suite for Config class"""
    
    def test_directories_created(self):
        """Test that all required directories are created"""
        Config.ensure_dirs()
        
        assert os.path.isdir(Config.DATA_DIR)
        assert os.path.isdir(Config.NSE_RAW_DIR)
        assert os.path.isdir(Config.BSE_RAW_DIR)
        assert os.path.isdir(Config.WATCHLIST_DIR)
        assert os.path.isdir(Config.LOGS_DIR)
    
    def test_logger_setup(self):
        """Test that logger is configured properly"""
        logger = Config.setup_logger("test_logger")
        
        assert isinstance(logger, logging.Logger)
        assert logger.level == Config.LOG_LEVEL
        assert len(logger.handlers) >= 1
    
    def test_trading_holidays_defined(self):
        """Test that trading holidays are properly defined"""
        assert isinstance(Config.TRADING_HOLIDAYS, list)
        assert len(Config.TRADING_HOLIDAYS) > 0
        # 2025 should have holidays
        assert any("2025" in h for h in Config.TRADING_HOLIDAYS)
    
    def test_progressive_spike_thresholds(self):
        """Test that strategy thresholds are correctly set"""
        ps = Config.PROGRESSIVE_SPIKE
        
        assert ps["delivery_pct_min"] == 50
        assert ps["delivery_turnover_min"] == 5000000
        assert ps["atw_min"] == 20000
    
    def test_exit_strategy_defined(self):
        """Test that exit strategy parameters exist"""
        es = Config.EXIT_STRATEGY
        
        assert "take_profit_pct" in es
        assert "stop_loss_pct" in es
        assert "time_stop_days" in es
        assert es["take_profit_pct"] == 12
        assert es["stop_loss_pct"] == -15
        assert es["time_stop_days"] == 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
