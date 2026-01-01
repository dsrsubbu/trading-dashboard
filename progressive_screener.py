import pandas as pd

class ProgressiveSpiker:
    """12-condition Progressive Spike screener for stock signals"""
    
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize screener with dataset.
        
        Args:
            df: DataFrame with columns: SYMBOL, CLOSE, DELIV_PER, DELIVERY_TURNOVER, ATW
                and optionally: DELIV_PER_1W/1M/3M, DELIVERY_TURNOVER_1W/1M/3M, ATW_1W/1M/3M
        """
        self.df = df
    
    def get_signals(self, strict_mode: bool = False) -> pd.DataFrame:
        """Filter stocks passing conditions
        
        Args:
            strict_mode: If True, requires all 12 conditions (Today > 1W > 1M > 3M).
                        If False, uses relaxed mode when insufficient history 
                        (only requires Today > 1W and 1W > 1M when 1M == 3M).
        
        Conditions:
        - Baseline (3): Delivery % >= 50, Delivery Turnover >= 5M, ATW >= 20K
        - Progressive (9): For each metric, Today > 1W > 1M > 3M
        
        Returns:
            DataFrame of stocks passing conditions
        """
        df = self.df.copy()
        
        required = ["SYMBOL", "CLOSE", "DELIV_PER", "DELIVERY_TURNOVER", "ATW"]
        if not all(col in df.columns for col in required):
            return pd.DataFrame()
        
        # Filter out bad data
        df = df[df["CLOSE"] > 0]
        df = df[df["DELIV_PER"] > 0]
        df = df[df["DELIVERY_TURNOVER"] > 0]
        df = df[df["ATW"] > 0]
        
        # Baseline 3 conditions (STRICT)
        df = df[df["DELIV_PER"] >= 50]
        df = df[df["DELIVERY_TURNOVER"] >= 5000000]
        df = df[df["ATW"] >= 20000]
        
        # Progressive conditions for DELIV_PER
        if all(col in df.columns for col in ["DELIV_PER_1W", "DELIV_PER_1M", "DELIV_PER_3M"]):
            if strict_mode:
                # Full 12-condition mode: Today > 1W > 1M > 3M
                df = df[(df["DELIV_PER"] > df["DELIV_PER_1W"]) & 
                        (df["DELIV_PER_1W"] > df["DELIV_PER_1M"]) & 
                        (df["DELIV_PER_1M"] > df["DELIV_PER_3M"])]
            else:
                # Relaxed mode: Today > 1W > 1M (skip 1M > 3M if they're equal due to limited data)
                df = df[(df["DELIV_PER"] > df["DELIV_PER_1W"]) & 
                        (df["DELIV_PER_1W"] > df["DELIV_PER_1M"])]
        
        # Progressive conditions for DELIVERY_TURNOVER
        if all(col in df.columns for col in ["DELIVERY_TURNOVER_1W", "DELIVERY_TURNOVER_1M", "DELIVERY_TURNOVER_3M"]):
            if strict_mode:
                df = df[(df["DELIVERY_TURNOVER"] > df["DELIVERY_TURNOVER_1W"]) & 
                        (df["DELIVERY_TURNOVER_1W"] > df["DELIVERY_TURNOVER_1M"]) & 
                        (df["DELIVERY_TURNOVER_1M"] > df["DELIVERY_TURNOVER_3M"])]
            else:
                df = df[(df["DELIVERY_TURNOVER"] > df["DELIVERY_TURNOVER_1W"]) & 
                        (df["DELIVERY_TURNOVER_1W"] > df["DELIVERY_TURNOVER_1M"])]
        
        # Progressive conditions for ATW
        if all(col in df.columns for col in ["ATW_1W", "ATW_1M", "ATW_3M"]):
            if strict_mode:
                df = df[(df["ATW"] > df["ATW_1W"]) & 
                        (df["ATW_1W"] > df["ATW_1M"]) & 
                        (df["ATW_1M"] > df["ATW_3M"])]
            else:
                df = df[(df["ATW"] > df["ATW_1W"]) & 
                        (df["ATW_1W"] > df["ATW_1M"])]
        
        return df.reset_index(drop=True)
    
    def get_baseline_signals(self) -> pd.DataFrame:
        """Filter stocks passing only baseline 3 conditions (for quick scanning)"""
        df = self.df.copy()
        
        required = ["SYMBOL", "CLOSE", "DELIV_PER", "DELIVERY_TURNOVER", "ATW"]
        if not all(col in df.columns for col in required):
            return pd.DataFrame()
        
        # Filter out bad data
        df = df[df["CLOSE"] > 0]
        df = df[df["DELIV_PER"] > 0]
        df = df[df["DELIVERY_TURNOVER"] > 0]
        df = df[df["ATW"] > 0]
        
        # Baseline 3 conditions only
        df = df[df["DELIV_PER"] >= 50]
        df = df[df["DELIVERY_TURNOVER"] >= 5000000]
        df = df[df["ATW"] >= 20000]
        
        return df.reset_index(drop=True)
