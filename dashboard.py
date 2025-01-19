import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="Football Data Analysis Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .original {
        background-color: #e6f3ff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #b8daff;
    }
    .new {
        background-color: #f0fff0;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #c3e6cb;
    }
    .task {
        background-color: #fff0f0;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #f5c6cb;
    }
    .highlight {
        background-color: #fffbea;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #ffeeba;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    excel_file = "Football Data Test Task.xlsx"
    raw_data = pd.read_excel(excel_file, sheet_name="Raw Data")
    processed_data = pd.read_excel(excel_file, sheet_name="Processed Data")
    manipulated_data = pd.read_excel(excel_file, sheet_name="Manipulated Data")
    return raw_data, processed_data, manipulated_data

raw_data, processed_data, manipulated_data = load_data()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Project Info", "Team Analysis", "Data Comparison", "Task Verification", "Detailed Analysis"]
)

if page == "Project Info":
    st.title("Football Data Analysis Project")
    
    # Project Overview
    st.header("Project Overview")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        This project processes and analyzes football match data to provide insights into team performance
        and match outcomes. The analysis includes:
        
        - Historical match data analysis
        - Team performance metrics
        - Rolling statistics calculation
        - Advanced performance indicators
        """)
        
    with col2:
        # Show basic dataset stats
        st.markdown('<div class="highlight">', unsafe_allow_html=True)
        st.subheader("Dataset Statistics")
        st.write(f"Total Matches: {len(processed_data):,}")
        st.write(f"Total Features: {len(processed_data.columns):,}")
        st.write(f"Date Range: {processed_data['Date'].min()} to {processed_data['Date'].max()}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Structure
    st.header("Data Structure")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="original">', unsafe_allow_html=True)
        st.subheader("Basic Match Details")
        st.markdown("""
        - Incremental_ID: Unique match identifier
        - Div: League division
        - Date & Time: Match timing
        - HomeTeam & AwayTeam: Participating teams
        - FTHG & FTAG: Full-time goals
        - FTR: Full-time result
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="new">', unsafe_allow_html=True)
        st.subheader("Performance Metrics")
        st.markdown("""
        Rolling statistics for last 5, 15, and 38 matches:
        - Goals scored and conceded
        - Shots and shots on target
        - Clean sheets and scoring records
        - Form and points
        - Discipline (cards)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Quality
    st.header("Data Quality Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        missing_values = processed_data.isnull().sum().sum()
        st.metric("Missing Values", missing_values)
    
    with col2:
        duplicates = len(processed_data[processed_data.duplicated()])
        st.metric("Duplicate Rows", duplicates)
    
    with col3:
        completeness = ((1 - processed_data.isnull().sum().sum() / (processed_data.shape[0] * processed_data.shape[1])) * 100)
        st.metric("Data Completeness", f"{completeness:.2f}%")
    
    # Sample Visualizations
    st.header("Sample Insights")
    
    # Home vs Away Win Distribution
    fig_results = px.pie(
        raw_data, 
        names='FTR',
        title='Match Outcomes Distribution (H: Home Win, A: Away Win, D: Draw)',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_results)
    
    # Goals Distribution
    fig_goals = go.Figure()
    fig_goals.add_trace(go.Histogram(x=raw_data['FTHG'], name='Home Goals'))
    fig_goals.add_trace(go.Histogram(x=raw_data['FTAG'], name='Away Goals'))
    fig_goals.update_layout(
        barmode='overlay',
        title='Distribution of Goals Scored',
        xaxis_title='Number of Goals',
        yaxis_title='Frequency'
    )
    fig_goals.update_traces(opacity=0.75)
    st.plotly_chart(fig_goals)

elif page == "Team Analysis":
    st.header("Team Analysis")
    
    # Enhanced team selector with more context
    col1, col2 = st.columns([2, 1])
    with col1:
        team = st.selectbox("Select a team", sorted(raw_data['HomeTeam'].unique()))
    with col2:
        window = st.selectbox("Select time window", [5, 15, 38])
    
    # Get team stats
    team_stats = processed_data[
        (processed_data['HomeTeam'] == team) | 
        (processed_data['AwayTeam'] == team)
    ].copy()
    
    # Overall Performance Metrics
    st.subheader("Overall Performance")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        home_goals = team_stats[f'Home_Goals_L{window}'].mean()
        away_goals = team_stats[f'Away_Goals_L{window}'].mean()
        st.metric("Avg Goals", f"{(home_goals + away_goals)/2:.2f}")
    
    with col2:
        home_wins = team_stats[f'Home_Wins_L{window}'].mean()
        away_wins = team_stats[f'Away_Wins_L{window}'].mean()
        st.metric("Avg Wins", f"{(home_wins + away_wins)/2:.2f}")
    
    with col3:
        home_form = team_stats[f'Home_Form_L{window}'].mean()
        away_form = team_stats[f'Away_Form_L{window}'].mean()
        st.metric("Form %", f"{(home_form + away_form)/2:.1f}%")
    
    with col4:
        home_clean = team_stats[f'Home_CleanSheets_L{window}'].mean()
        away_clean = team_stats[f'Away_CleanSheets_L{window}'].mean()
        st.metric("Clean Sheets", f"{(home_clean + away_clean)/2:.2f}")
    
    # Detailed Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        # Shooting Efficiency
        fig_shooting = go.Figure()
        fig_shooting.add_trace(go.Scatter(
            y=team_stats[f'Home_ShotConversion_L{window}'],
            name='Shot Conversion %',
            line=dict(color='blue')
        ))
        fig_shooting.add_trace(go.Scatter(
            y=team_stats[f'Home_ShotAccuracy_L{window}'],
            name='Shot Accuracy %',
            line=dict(color='green')
        ))
        fig_shooting.update_layout(title=f"{team}'s Shooting Efficiency")
        st.plotly_chart(fig_shooting)
    
    with col2:
        # Form Analysis
        fig_form = go.Figure()
        fig_form.add_trace(go.Scatter(
            y=team_stats[f'Home_Form_L{window}'],
            name='Home Form',
            line=dict(color='blue')
        ))
        fig_form.add_trace(go.Scatter(
            y=team_stats[f'Away_Form_L{window}'],
            name='Away Form',
            line=dict(color='red')
        ))
        fig_form.update_layout(title=f"{team}'s Form Analysis")
        st.plotly_chart(fig_form)
    
    # Discipline Analysis
    st.subheader("Discipline Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cards = go.Figure()
        fig_cards.add_trace(go.Bar(
            name='Yellow Cards',
            x=['Home', 'Away'],
            y=[
                team_stats[f'Home_YellowCards_L{window}'].mean(),
                team_stats[f'Away_YellowCards_L{window}'].mean()
            ]
        ))
        fig_cards.add_trace(go.Bar(
            name='Red Cards',
            x=['Home', 'Away'],
            y=[
                team_stats[f'Home_RedCards_L{window}'].mean(),
                team_stats[f'Away_RedCards_L{window}'].mean()
            ]
        ))
        fig_cards.update_layout(title=f"{team}'s Card Analysis", barmode='group')
        st.plotly_chart(fig_cards)
    
    with col2:
        # Fouls Analysis
        fig_fouls = go.Figure()
        fig_fouls.add_trace(go.Box(
            y=team_stats[f'Home_Fouls_L{window}'],
            name='Home Fouls'
        ))
        fig_fouls.add_trace(go.Box(
            y=team_stats[f'Away_Fouls_L{window}'],
            name='Away Fouls'
        ))
        fig_fouls.update_layout(title=f"{team}'s Fouls Distribution")
        st.plotly_chart(fig_fouls)

elif page == "Data Comparison":
    st.header("Data Comparison")
    
    # Enhanced comparison tools
    st.subheader("Calculation Verification")
    
    col1, col2 = st.columns(2)
    with col1:
        team = st.selectbox("Select Team", sorted(raw_data['HomeTeam'].unique()))
    with col2:
        stat = st.selectbox("Select Statistic", [
            'Goals', 'Wins', 'Shots', 'ShotsOnTarget', 'Corners', 'Fouls'
        ])
    
    # Compare calculations
    comparison_data = processed_data[
        (processed_data['HomeTeam'] == team) | 
        (processed_data['AwayTeam'] == team)
    ].head(10)
    
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.write(f"Last 10 matches for {team}")
    st.write(comparison_data[[
        'Date', 'HomeTeam', 'AwayTeam',
        f'Home_{stat}_L5', f'Away_{stat}_L5'
    ]])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualization of comparison
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(
        y=comparison_data[f'Home_{stat}_L5'],
        name=f'Home {stat}',
        line=dict(color='blue')
    ))
    fig_comp.add_trace(go.Scatter(
        y=comparison_data[f'Away_{stat}_L5'],
        name=f'Away {stat}',
        line=dict(color='red')
    ))
    fig_comp.update_layout(title=f"{team}'s {stat} Comparison")
    st.plotly_chart(fig_comp)

elif page == "Task Verification":
    st.header("Task Verification")
    
    # Original Requirements
    st.markdown('<div class="task">', unsafe_allow_html=True)
    st.subheader("Original Requirements")
    st.markdown("""
    1. Process blue columns from Raw Data
    2. Calculate rolling statistics (5, 15, 38 matches)
    3. Include both home and away matches
    4. Calculate for both teams in each match
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Implementation Details
    st.markdown('<div class="new">', unsafe_allow_html=True)
    st.subheader("Implementation")
    st.markdown("""
    Processed all required columns
    Calculated rolling statistics for all windows
    Included both home and away matches
    Added advanced metrics:
    - Goal difference and points
    - Shot conversion rates
    - Form percentage
    - Clean sheets
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Quality Checks
    st.subheader("Data Quality Verification")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Rows Processed",
            len(processed_data),
            f"{len(processed_data) - len(raw_data):+d}"
        )
    
    with col2:
        st.metric(
            "Columns Added",
            len(processed_data.columns),
            f"{len(processed_data.columns) - len(raw_data.columns):+d}"
        )
    
    with col3:
        completeness = (1 - processed_data.isnull().sum().sum() / 
                       (processed_data.shape[0] * processed_data.shape[1])) * 100
        st.metric("Data Completeness", f"{completeness:.1f}%")

else:  # Detailed Analysis
    st.header("Detailed Analysis")
    
    # Data Understanding Section
    st.subheader("1. Data Understanding and Predictive Modeling")
    
    # Q1: Information in Processed Data
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.write("**Q: What information is captured in the Processed Data sheet?**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        The dataset contains:
        1. **Match Identifiers**:
           - Incremental_ID, Date, Time
           - HomeTeam, AwayTeam
        
        2. **Match Outcomes**:
           - FTHG: Full Time Home Goals
           - FTAG: Full Time Away Goals
           - FTR: Full Time Result (H/A/D)
        
        3. **Performance Metrics**:
           - Goals, Shots, Corners
           - Cards, Fouls
           - Form and Points
        
        4. **Rolling Statistics**:
           - Last 5 matches (L5)
           - Last 15 matches (L15)
           - Last 38 matches (L38)
        """)
    
    with col2:
        # Show feature categories and their counts
        feature_categories = {
            'Match Info': len([col for col in processed_data.columns if col in ['Date', 'Time', 'HomeTeam', 'AwayTeam']]),
            'Goals': len([col for col in processed_data.columns if 'Goal' in col]),
            'Shots': len([col for col in processed_data.columns if 'Shot' in col]),
            'Cards': len([col for col in processed_data.columns if 'Card' in col]),
            'Form': len([col for col in processed_data.columns if 'Form' in col])
        }
        fig = px.bar(
            x=list(feature_categories.keys()),
            y=list(feature_categories.values()),
            title='Feature Distribution by Category',
            labels={'x': 'Category', 'y': 'Number of Features'}
        )
        st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Q2: Team Performance Analysis
    st.markdown('<div class="original">', unsafe_allow_html=True)
    st.write("**Q: Most relevant columns for team performance analysis?**")
    
    # Calculate correlation matrix for key metrics
    performance_cols = [
        'FTHG', 'FTAG', 'Home_Goals_L5', 'Away_Goals_L5',
        'Home_ShotConversion_L5', 'Away_ShotConversion_L5',
        'Home_Form_L5', 'Away_Form_L5'
    ]
    corr_matrix = processed_data[performance_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        title='Correlation Matrix of Key Performance Metrics',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig)
    
    st.markdown("""
    Key performance indicators by importance:
    1. Recent Form (L5) - strongest predictor
    2. Goal Scoring Rate
    3. Shot Conversion
    4. Historical Performance (L38)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Cleaning Section
    st.subheader("2. Data Cleaning and Preprocessing")
    
    # Normalization Strategies
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.write("**Normalization Strategies for Performance Metrics**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Recommended Approaches:**
        1. **Min-Max Scaling** for bounded metrics:
           - Form percentages (0-100%)
           - Shot accuracy rates
           - Conversion rates
        
        2. **Standard Scaling** for unbounded metrics:
           - Goals scored
           - Shots taken
           - Corner counts
        
        3. **Robust Scaling** for metrics with outliers:
           - Cards received
           - Fouls committed
        """)
        
        # Example of different scaling methods
        example_metric = processed_data['Home_Form_L38'].dropna()
        scaled_data = pd.DataFrame({
            'Original': example_metric,
            'MinMax': (example_metric - example_metric.min()) / (example_metric.max() - example_metric.min()),
            'Standard': (example_metric - example_metric.mean()) / example_metric.std()
        })
        
        fig = go.Figure()
        for col in scaled_data.columns:
            fig.add_trace(go.Box(y=scaled_data[col], name=col))
        fig.update_layout(title='Comparison of Scaling Methods')
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        **Handling Special Cases:**
        1. **Percentage Metrics:**
           - Already normalized (0-100%)
           - Check for consistency
           - Handle extreme values
        
        2. **Cumulative Metrics:**
           - Normalize by games played
           - Consider seasonal effects
        
        3. **Rate Metrics:**
           - Use per-game calculations
           - Handle division by zero
        """)
        
        # Show distribution before and after normalization
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=processed_data['Home_Form_L38'],
            name='Before Normalization',
            opacity=0.75
        ))
        fig.add_trace(go.Histogram(
            x=(processed_data['Home_Form_L38'] - processed_data['Home_Form_L38'].mean()) / 
              processed_data['Home_Form_L38'].std(),
            name='After Normalization',
            opacity=0.75
        ))
        fig.update_layout(
            title='Distribution Before and After Normalization',
            barmode='overlay'
        )
        st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Validation of Aggregated Statistics
    st.markdown('<div class="original">', unsafe_allow_html=True)
    st.write("**Validating Reliability of Aggregated Statistics**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Validation Approaches:**
        1. **Cross-Validation:**
           - Time-based splitting
           - Rolling window validation
           - Out-of-sample testing
        
        2. **Statistical Tests:**
           - Confidence intervals
           - Hypothesis testing
           - Variance analysis
        
        3. **Domain Validation:**
           - Compare with expected ranges
           - Expert review
           - Historical benchmarking
        """)
        
        # Example: Confidence Intervals
        team_stats = processed_data.groupby('HomeTeam')['Home_Goals_L38'].mean()
        team_std = processed_data.groupby('HomeTeam')['Home_Goals_L38'].std()
        confidence = 0.95
        z_score = 1.96  # 95% confidence interval
        
        ci_lower = team_stats - z_score * (team_std / np.sqrt(len(team_stats)))
        ci_upper = team_stats + z_score * (team_std / np.sqrt(len(team_stats)))
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=team_stats,
            name='Team Goals',
            boxpoints='all'
        ))
        
        # Add error bars for confidence intervals
        fig.add_trace(go.Scatter(
            x=team_stats.index,
            y=team_stats,
            error_y=dict(
                type='data',
                symmetric=False,
                array=ci_upper - team_stats,
                arrayminus=team_stats - ci_lower
            ),
            mode='markers',
            name='95% CI',
            marker=dict(color='red', size=8)
        ))
        
        fig.update_layout(
            title='Team Goals with 95% Confidence Intervals',
            yaxis_title='Average Goals',
            showlegend=True
        )
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        **Quality Checks:**
        1. **Temporal Consistency:**
           - Check for seasonal patterns
           - Identify anomalies
           - Verify trend stability
        
        2. **Sample Size:**
           - Minimum games threshold
           - Statistical significance
           - Confidence levels
        
        3. **Edge Cases:**
           - New teams in league
           - Team form changes
           - Rare events
        """)
        
        # Show sample size effect
        sample_sizes = [5, 15, 38]
        variances = []
        for size in sample_sizes:
            stat_name = f'Home_Goals_L{size}'
            variances.append(processed_data[stat_name].std())
        
        fig = px.bar(
            x=['Last 5', 'Last 15', 'Last 38'],
            y=variances,
            title='Statistical Variance by Sample Size',
            labels={'x': 'Sample Size', 'y': 'Standard Deviation'}
        )
        st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Missing Values Analysis
    st.markdown('<div class="new">', unsafe_allow_html=True)
    st.write("**Missing Values Analysis**")
    
    missing_data = processed_data.isnull().sum()
    missing_pct = (missing_data / len(processed_data)) * 100
    
    fig = px.bar(
        x=missing_pct[missing_pct > 0].index,
        y=missing_pct[missing_pct > 0].values,
        title='Percentage of Missing Values by Column',
        labels={'x': 'Column', 'y': 'Missing %'}
    )
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Distribution
    st.markdown('<div class="new">', unsafe_allow_html=True)
    st.write("**Data Distribution Analysis**")
    
    # Show distribution of a key metric
    fig = px.histogram(
        processed_data,
        x='Home_Form_L38',
        title='Distribution of Home Form (L38)',
        labels={'Home_Form_L38': 'Form %'},
        marginal='box'
    )
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Engineering Section
    st.subheader("3. Feature Engineering and Impact Analysis")
    
    # Cards Impact Analysis
    st.markdown('<div class="task">', unsafe_allow_html=True)
    st.write("**Impact of Cards on Match Outcomes**")
    
    col1, col2 = st.columns(2)
    with col1:
        # Calculate win rate by card ranges
        processed_data['YellowCard_Level'] = pd.qcut(
            processed_data['Home_YellowCards_L5'],
            q=4,
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        win_rate = processed_data.groupby('YellowCard_Level')['FTR'].apply(
            lambda x: (x == 'H').mean() * 100
        )
        
        fig = px.bar(
            x=win_rate.index,
            y=win_rate.values,
            title='Home Win Rate by Yellow Card History',
            labels={'x': 'Yellow Card Level', 'y': 'Win Rate (%)'}
        )
        st.plotly_chart(fig)
    
    with col2:
        # Red Card Analysis
        red_card_impact = processed_data.groupby(
            processed_data['Home_RedCards_L5'] > 0
        )['FTR'].apply(lambda x: (x == 'H').mean() * 100)
        
        fig = px.bar(
            x=['No Red Cards', 'Has Red Cards'],
            y=red_card_impact.values,
            title='Win Rate: Impact of Recent Red Cards',
            labels={'x': 'Red Card History', 'y': 'Win Rate (%)'}
        )
        st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Time-based Analysis
    st.subheader("4. Time-based Analysis and Trends")
    
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Seasonal Trends
        processed_data['Month'] = pd.to_datetime(processed_data['Date']).dt.month
        monthly_stats = processed_data.groupby('Month').agg({
            'FTHG': 'mean',
            'FTAG': 'mean',
            'Home_Form_L5': 'mean'
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_stats.index,
            y=monthly_stats['FTHG'],
            name='Home Goals',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=monthly_stats.index,
            y=monthly_stats['FTAG'],
            name='Away Goals',
            line=dict(color='red')
        ))
        fig.update_layout(
            title='Seasonal Scoring Trends',
            xaxis_title='Month',
            yaxis_title='Average Goals'
        )
        st.plotly_chart(fig)
    
    with col2:
        # Form Trends
        fig = px.line(
            monthly_stats,
            y='Home_Form_L5',
            title='Home Team Form Trends by Month',
            labels={'Home_Form_L5': 'Average Form %'}
        )
        st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Model Considerations
    st.subheader("5. Machine Learning Considerations")
    
    st.markdown('<div class="original">', unsafe_allow_html=True)
    st.write("**Key Considerations for Model Development**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Data Processing:**
        1. Handle temporal dependencies
        2. Feature scaling for metrics
        3. Encoding categorical variables
        4. Cross-validation strategy
        """)
        
        # Show class distribution
        fig = px.pie(
            processed_data,
            names='FTR',
            title='Target Variable Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig)
    
    with col2:
        st.markdown("""
        **Feature Selection Priority:**
        1. Recent form and performance
        2. Head-to-head history
        3. Team-specific metrics
        4. Seasonal trends
        """)
        
        # Feature importance simulation
        feature_importance = {
            'Recent Form': 0.35,
            'Goal Scoring': 0.25,
            'Defense': 0.20,
            'Historical': 0.15,
            'Other': 0.05
        }
        
        fig = px.bar(
            x=list(feature_importance.keys()),
            y=list(feature_importance.values()),
            title='Simulated Feature Importance',
            labels={'x': 'Feature Category', 'y': 'Importance Score'}
        )
        st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("### Contact Information")

# Custom CSS for social links
st.markdown("""
<style>
.social-links {
    display: flex;
    gap: 10px;
    margin: 10px 0;
    flex-wrap: wrap;
}
.social-links a {
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# Generate social links with badges
social_links = f"""
<div class="social-links">
    <a href="https://www.linkedin.com/in/sanket-jagtap-966116283/" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
    </a>
    <a href="https://github.com/Jsan2002" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
    </a>
    <a href="mailto:sanketjagtap2002@gmail.com">
        <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
    </a>
</div>
"""

st.markdown(social_links, unsafe_allow_html=True)

# Add copyright and credits
st.markdown("---")
st.markdown(" 2025 Sanket Jagtap • Built with Streamlit and Python")
