import pandas as pd
import numpy as np

def calculate_team_stats(df, team, n_matches):
    """Calculate statistics for a team over their last N matches."""
    team_matches = df[
        (df['HomeTeam'] == team) | (df['AwayTeam'] == team)
    ].copy()
    
    team_matches = team_matches.sort_values('Incremental_ID')
    stats = {}
    
    for idx in df.index:
        current_match = team_matches[team_matches.index <= idx]
        last_n = current_match.tail(n_matches)
        
        # Basic Stats
        home_goals = last_n[last_n['HomeTeam'] == team]['FTHG'].sum()
        away_goals = last_n[last_n['AwayTeam'] == team]['FTAG'].sum()
        stats.setdefault(f'Goals_L{n_matches}', {})[idx] = home_goals + away_goals
        
        # Goals Conceded
        home_conceded = last_n[last_n['HomeTeam'] == team]['FTAG'].sum()
        away_conceded = last_n[last_n['AwayTeam'] == team]['FTHG'].sum()
        stats.setdefault(f'GoalsConceded_L{n_matches}', {})[idx] = home_conceded + away_conceded
        
        # Goal Difference
        stats.setdefault(f'GoalDiff_L{n_matches}', {})[idx] = (home_goals + away_goals) - (home_conceded + away_conceded)
        
        # Results
        home_wins = len(last_n[(last_n['HomeTeam'] == team) & (last_n['FTR'] == 'H')])
        away_wins = len(last_n[(last_n['AwayTeam'] == team) & (last_n['FTR'] == 'A')])
        stats.setdefault(f'Wins_L{n_matches}', {})[idx] = home_wins + away_wins
        
        home_draws = len(last_n[(last_n['HomeTeam'] == team) & (last_n['FTR'] == 'D')])
        away_draws = len(last_n[(last_n['AwayTeam'] == team) & (last_n['FTR'] == 'D')])
        stats.setdefault(f'Draws_L{n_matches}', {})[idx] = home_draws + away_draws
        
        home_losses = len(last_n[(last_n['HomeTeam'] == team) & (last_n['FTR'] == 'A')])
        away_losses = len(last_n[(last_n['AwayTeam'] == team) & (last_n['FTR'] == 'H')])
        stats.setdefault(f'Losses_L{n_matches}', {})[idx] = home_losses + away_losses
        
        # Points (3 for win, 1 for draw)
        points = (home_wins + away_wins) * 3 + (home_draws + away_draws)
        stats.setdefault(f'Points_L{n_matches}', {})[idx] = points
        
        # Shooting Stats
        home_shots = last_n[last_n['HomeTeam'] == team]['HS'].sum()
        away_shots = last_n[last_n['AwayTeam'] == team]['AS'].sum()
        stats.setdefault(f'Shots_L{n_matches}', {})[idx] = home_shots + away_shots
        
        home_shots_target = last_n[last_n['HomeTeam'] == team]['HST'].sum()
        away_shots_target = last_n[last_n['AwayTeam'] == team]['AST'].sum()
        stats.setdefault(f'ShotsOnTarget_L{n_matches}', {})[idx] = home_shots_target + away_shots_target
        
        # Shot Conversion Rate (%)
        total_shots = home_shots + away_shots
        shot_conversion = ((home_goals + away_goals) / total_shots * 100) if total_shots > 0 else 0
        stats.setdefault(f'ShotConversion_L{n_matches}', {})[idx] = shot_conversion
        
        # Shot Accuracy (%)
        shots_on_target = home_shots_target + away_shots_target
        shot_accuracy = (shots_on_target / total_shots * 100) if total_shots > 0 else 0
        stats.setdefault(f'ShotAccuracy_L{n_matches}', {})[idx] = shot_accuracy
        
        # Set Pieces
        home_corners = last_n[last_n['HomeTeam'] == team]['HC'].sum()
        away_corners = last_n[last_n['AwayTeam'] == team]['AC'].sum()
        stats.setdefault(f'Corners_L{n_matches}', {})[idx] = home_corners + away_corners
        
        # Discipline
        home_fouls = last_n[last_n['HomeTeam'] == team]['HF'].sum()
        away_fouls = last_n[last_n['AwayTeam'] == team]['AF'].sum()
        stats.setdefault(f'Fouls_L{n_matches}', {})[idx] = home_fouls + away_fouls
        
        home_yellows = last_n[last_n['HomeTeam'] == team]['HY'].sum()
        away_yellows = last_n[last_n['AwayTeam'] == team]['AY'].sum()
        stats.setdefault(f'YellowCards_L{n_matches}', {})[idx] = home_yellows + away_yellows
        
        home_reds = last_n[last_n['HomeTeam'] == team]['HR'].sum()
        away_reds = last_n[last_n['AwayTeam'] == team]['AR'].sum()
        stats.setdefault(f'RedCards_L{n_matches}', {})[idx] = home_reds + away_reds
        
        # Form (percentage of available points won)
        max_points = len(last_n) * 3
        form = (points / max_points * 100) if max_points > 0 else 0
        stats.setdefault(f'Form_L{n_matches}', {})[idx] = form
        
        # Clean Sheets
        home_clean = len(last_n[(last_n['HomeTeam'] == team) & (last_n['FTAG'] == 0)])
        away_clean = len(last_n[(last_n['AwayTeam'] == team) & (last_n['FTHG'] == 0)])
        stats.setdefault(f'CleanSheets_L{n_matches}', {})[idx] = home_clean + away_clean
        
        # Failed to Score
        home_blank = len(last_n[(last_n['HomeTeam'] == team) & (last_n['FTHG'] == 0)])
        away_blank = len(last_n[(last_n['AwayTeam'] == team) & (last_n['FTAG'] == 0)])
        stats.setdefault(f'FailedToScore_L{n_matches}', {})[idx] = home_blank + away_blank
    
    return stats

def process_all_teams(df):
    """Process all teams and calculate their statistics."""
    processed_df = df.copy()
    
    # Get unique teams
    all_teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    
    # Calculate statistics for each team
    team_stats = {}
    for team in all_teams:
        print(f'Processing {team}...')
        team_stats[team] = {
            5: calculate_team_stats(df, team, 5),
            15: calculate_team_stats(df, team, 15),
            38: calculate_team_stats(df, team, 38)
        }
    
    # Add statistics to the dataframe
    for idx, row in processed_df.iterrows():
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']
        
        # Add home team stats
        for n in [5, 15, 38]:
            for stat_name, stat_values in team_stats[home_team][n].items():
                col_name = f'Home_{stat_name}'
                if idx in stat_values:
                    processed_df.at[idx, col_name] = stat_values[idx]
        
        # Add away team stats
        for n in [5, 15, 38]:
            for stat_name, stat_values in team_stats[away_team][n].items():
                col_name = f'Away_{stat_name}'
                if idx in stat_values:
                    processed_df.at[idx, col_name] = stat_values[idx]
    
    return processed_df

def main():
    # Read the Excel file
    print('Reading data...')
    df_raw = pd.read_excel('Football Data Test Task.xlsx', sheet_name='Raw Data')
    print(f'Raw data shape: {df_raw.shape}')
    
    # Process all teams
    print('\nProcessing teams...')
    processed_df = process_all_teams(df_raw)
    
    # Save to Excel
    print('\nSaving results...')
    with pd.ExcelWriter('Football Data Test Task.xlsx', mode='a', 
                       if_sheet_exists='replace', engine='openpyxl') as writer:
        processed_df.to_excel(writer, sheet_name='Processed Data', index=False)
    
    # Print new columns
    print('\nNew columns added:')
    new_cols = [col for col in processed_df.columns if col not in df_raw.columns]
    print('\n'.join(new_cols))
    
    print('\nDone! Check the "Processed Data" sheet in the Excel file.')

if __name__ == "__main__":
    main()
