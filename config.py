# Configuration settings for the Streamlit app

# Default column configurations
COLUMN_CONFIGS = {
    'personal_info': {
        'columns': ['prefix', 'first_name', 'last_name', 'full_name', 'email', 'phone'],
        'width': 150,
        'pinned': ['first_name', 'last_name']
    },
    'address': {
        'columns': ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country'],
        'width': 120
    },
    'disc_profile': {
        'columns': [
            'disc_profile', 'disc_sales', 'disc_communication', 'leadership_style',
            'team_dynamics', 'conflict_resolution', 'customer_service_approach',
            'decision_making_style', 'workplace_behavior', 'hiring_and_recruitment',
            'coaching_and_development'
        ],
        'width': 180,
        'wrap_text': True
    },
    'company': {
        'columns': ['company_id', 'industry', 'position', 'company_size', 'website'],
        'width': 140
    },
    'dates': {
        'columns': ['date_of_birth', 'assessment_date'],
        'width': 120
    }
}

# AgGrid theme options
AGGRID_THEMES = ['streamlit', 'alpine', 'balham', 'material']

# Default refresh intervals (in seconds)
REFRESH_INTERVALS = [10, 30, 60, 120, 300]
