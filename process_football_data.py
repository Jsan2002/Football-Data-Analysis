import pandas as pd
import numpy as np

def calculate_rolling_stats(df, team_col, match_counts=[5, 15, 38]):
    """Calculate rolling statistics for each team."""
    teams = df[team_col].unique()
    all_stats = {}
    
    for team in teams:
        # Get matches where the team played (either home or away)
        team_matches = df[
            (df['HomeTeam'] == team) | (df['AwayTeam'] == team)
        ].copy()
        
        # Sort by index (assuming matches are in chronological order)
        team_matches = team_matches.sort_index()
        
        for n in match_counts:
            # Calculate rolling stats for different window sizes
            suffix = f'_L{n}'
            
            # Initialize stats for this window size
            if n not in all_stats:
                all_stats[n] = {}
            
            # Calculate various statistics
            for stat in ['FTHG', 'FTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 
                        'HC', 'AC', 'HY', 'AY', 'HR', 'AR']:
                # Calculate sum for when team is home
                home_mask = team_matches['HomeTeam'] == team
                away_mask = team_matches['AwayTeam'] == team
                
                # Get the relevant column based on whether team is home or away
                values = pd.Series(index=team_matches.index, dtype=float)
                
                if stat.startswith('H'):
                    values[home_mask] = team_matches.loc[home_mask, stat]
                    away_stat = 'A' + stat[1:]
                    values[away_mask] = team_matches.loc[away_mask, away_stat]
                else:
                    values[away_mask] = team_matches.loc[away_mask, stat]
                    home_stat = 'H' + stat[1:]
                    values[home_mask] = team_matches.loc[home_mask, home_stat]
                
                # Calculate rolling sum
                rolling_sum = values.rolling(window=n, min_periods=1).sum()
                
                # Store in all_stats
                if team not in all_stats[n]:
                    all_stats[n][team] = {}
                all_stats[n][team][stat + suffix] = rolling_sum
                
            # Calculate wins, losses, draws
            for result_type in ['W', 'L', 'D']:
                home_count = 0
                away_count = 0
                
                if result_type == 'W':
                    home_count = ((team_matches['HomeTeam'] == team) & (team_matches['FTR'] == 'H')).rolling(window=n, min_periods=1).sum()
                    away_count = ((team_matches['AwayTeam'] == team) & (team_matches['FTR'] == 'A')).rolling(window=n, min_periods=1).sum()
                elif result_type == 'L':
                    home_count = ((team_matches['HomeTeam'] == team) & (team_matches['FTR'] == 'A')).rolling(window=n, min_periods=1).sum()
                    away_count = ((team_matches['AwayTeam'] == team) & (team_matches['FTR'] == 'H')).rolling(window=n, min_periods=1).sum()
                else:  # Draws
                    home_count = ((team_matches['HomeTeam'] == team) & (team_matches['FTR'] == 'D')).rolling(window=n, min_periods=1).sum()
                    away_count = ((team_matches['AwayTeam'] == team) & (team_matches['FTR'] == 'D')).rolling(window=n, min_periods=1).sum()
                
                all_stats[n][team][f'H{result_type}{suffix}'] = home_count
                all_stats[n][team][f'A{result_type}{suffix}'] = away_count
    
    return all_stats

def process_football_data(input_file, sheet_name='Raw Data'):
    """Main function to process football data."""
    # Read the Excel file
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    
    # Calculate stats for both home and away teams
    home_stats = calculate_rolling_stats(df, 'HomeTeam')
    away_stats = calculate_rolling_stats(df, 'AwayTeam')
    
    # Create new columns in the dataframe
    for n in [5, 15, 38]:
        for team_idx, row in df.iterrows():
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            
            # Add home team stats
            if home_team in home_stats[n]:
                for stat, values in home_stats[n][home_team].items():
                    if team_idx in values.index:
                        df.at[team_idx, stat] = values[team_idx]
            
            # Add away team stats
            if away_team in away_stats[n]:
                for stat, values in away_stats[n][away_team].items():
                    if team_idx in values.index:
                        df.at[team_idx, stat] = values[team_idx]
    
    # Save the processed data to a new sheet
    with pd.ExcelWriter(input_file, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Processed Data', index=False)

if __name__ == "__main__":
    input_file = "Football Data Test Task.xlsx"
    process_football_data(input_file)
