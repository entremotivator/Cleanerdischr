"""
DISC Profile Analysis utilities
"""
import pandas as pd
import streamlit as st

def analyze_disc_profile(df):
    """Analyze DISC profile data and provide insights"""
    if 'disc_profile' not in df.columns:
        return None
   
    analysis = {
        'profile_distribution': df['disc_profile'].value_counts(),
        'leadership_styles': df['leadership_style'].value_counts() if 'leadership_style' in df.columns else None,
        'team_dynamics': df['team_dynamics'].value_counts() if 'team_dynamics' in df.columns else None,
        'communication_styles': df['disc_communication'].value_counts() if 'disc_communication' in df.columns else None
    }
   
    return analysis

def get_disc_insights(profile):
    """Get insights for specific DISC profile"""
    insights = {
        'D': {
            'name': 'Dominance',
            'traits': ['Direct', 'Results-oriented', 'Decisive', 'Competitive'],
            'strengths': ['Leadership', 'Problem-solving', 'Quick decisions'],
            'development': ['Patience', 'Collaboration', 'Active listening']
        },
        'I': {
            'name': 'Influence',
            'traits': ['Enthusiastic', 'Optimistic', 'People-oriented', 'Persuasive'],
            'strengths': ['Communication', 'Motivation', 'Team building'],
            'development': ['Follow-through', 'Detail attention', 'Time management']
        },
        'S': {
            'name': 'Steadiness',
            'traits': ['Patient', 'Reliable', 'Supportive', 'Consistent'],
            'strengths': ['Teamwork', 'Loyalty', 'Stability'],
            'development': ['Adaptability', 'Assertiveness', 'Change management']
        },
        'C': {
            'name': 'Conscientiousness',
            'traits': ['Analytical', 'Precise', 'Systematic', 'Quality-focused'],
            'strengths': ['Accuracy', 'Planning', 'Quality control'],
            'development': ['Flexibility', 'Risk-taking', 'Quick decisions']
        }
    }
   
    return insights.get(profile, {})

def display_disc_dashboard(df):
    """Display DISC profile dashboard"""
    st.subheader("🎯 DISC Profile Dashboard")
   
    analysis = analyze_disc_profile(df)
    if not analysis:
        st.warning("No DISC profile data available")
        return
   
    # Profile distribution

    col1, col2 = st.columns(2)
   
    with col1:
        st.write("**Profile Distribution:**")
        for profile, count in analysis['profile_distribution'].items():
            insights = get_disc_insights(profile)
            st.write(f"**{profile} - {insights.get('name', 'Unknown')}**: {count}")
   
    with col2:
        st.bar_chart(analysis['profile_distribution'])
   
    # Detailed insights
    if len(analysis['profile_distribution']) > 0:
        selected_profile = st.selectbox(
            "Select profile for detailed insights:",
            analysis['profile_distribution'].index.tolist()
        )
       
        insights = get_disc_insights(selected_profile)
        if insights:
            col1, col2, col3 = st.columns(3)
           
            with col1:
                st.write("**Key Traits:**")
                for trait in insights['traits']:
                    st.write(f"• {trait}")
           
            with col2:
                st.write("**Strengths:**")
                for strength in insights['strengths']:
                    st.write(f"• {strength}")
           
            with col3:
                st.write("**Development Areas:**")
                for area in insights['development']:
                    st.write(f"• {area}")
"""
DISC Profile Analysis utilities
"""
import pandas as pd
import streamlit as st

def analyze_disc_profile(df):
    """Analyze DISC profile data and provide insights"""
    if 'disc_profile' not in df.columns:
        return None
   
    analysis = {
        'profile_distribution': df['disc_profile'].value_counts(),
        'leadership_styles': df['leadership_style'].value_counts() if 'leadership_style' in df.columns else None,
        'team_dynamics': df['team_dynamics'].value_counts() if 'team_dynamics' in df.columns else None,
        'communication_styles': df['disc_communication'].value_counts() if 'disc_communication' in df.columns else None
    }
   
    return analysis

def get_disc_insights(profile):
    """Get insights for specific DISC profile"""
    insights = {
        'D': {
            'name': 'Dominance',
            'traits': ['Direct', 'Results-oriented', 'Decisive', 'Competitive'],
            'strengths': ['Leadership', 'Problem-solving', 'Quick decisions'],
            'development': ['Patience', 'Collaboration', 'Active listening']
        },
        'I': {
            'name': 'Influence',
            'traits': ['Enthusiastic', 'Optimistic', 'People-oriented', 'Persuasive'],
            'strengths': ['Communication', 'Motivation', 'Team building'],
            'development': ['Follow-through', 'Detail attention', 'Time management']
        },
        'S': {
            'name': 'Steadiness',
            'traits': ['Patient', 'Reliable', 'Supportive', 'Consistent'],
            'strengths': ['Teamwork', 'Loyalty', 'Stability'],
            'development': ['Adaptability', 'Assertiveness', 'Change management']
        },
        'C': {
            'name': 'Conscientiousness',
            'traits': ['Analytical', 'Precise', 'Systematic', 'Quality-focused'],
            'strengths': ['Accuracy', 'Planning', 'Quality control'],
            'development': ['Flexibility', 'Risk-taking', 'Quick decisions']
        }
    }
   
    return insights.get(profile, {})

def display_disc_dashboard(df):
    """Display DISC profile dashboard"""
    st.subheader("🎯 DISC Profile Dashboard")
   
    analysis = analyze_disc_profile(df)
    if not analysis:
        st.warning("No DISC profile data available")
        return
   
    # Profile distribution

    col1, col2 = st.columns(2)
   
    with col1:
        st.write("**Profile Distribution:**")
        for profile, count in analysis['profile_distribution'].items():
            insights = get_disc_insights(profile)
            st.write(f"**{profile} - {insights.get('name', 'Unknown')}**: {count}")
   
    with col2:
        st.bar_chart(analysis['profile_distribution'])
   
    # Detailed insights
    if len(analysis['profile_distribution']) > 0:
        selected_profile = st.selectbox(
            "Select profile for detailed insights:",
            analysis['profile_distribution'].index.tolist()
        )
       
        insights = get_disc_insights(selected_profile)
        if insights:
            col1, col2, col3 = st.columns(3)
           
            with col1:
                st.write("**Key Traits:**")
                for trait in insights['traits']:
                    st.write(f"• {trait}")
           
            with col2:
                st.write("**Strengths:**")
                for strength in insights['strengths']:
                    st.write(f"• {strength}")
           
            with col3:
                st.write("**Development Areas:**")
                for area in insights['development']:
                    st.write(f"• {area}")
