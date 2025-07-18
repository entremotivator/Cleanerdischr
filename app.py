import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import requests
from io import StringIO
import re

def get_sample_data():
    """Create sample data with the provided example"""
    sample_data = {
        'prefix': ['Mr.'],
        'first_name': ['John'],
        'last_name': ['Doe'],
        'full_name': ['John Doe'],
        'email': ['john.doe@example.com'],
        'timezone': ['America/New_York'],
        'address_line_1': ['123 Main Street'],
        'address_line_2': ['Apt 4B'],
        'city': ['New York'],
        'state': ['NY'],
        'postal_code': ['10001'],
        'country': ['United States'],
        'ip': ['192.168.1.1'],
        'phone': ['+1-555-123-4567'],
        'source': ['n8n_workflow'],
        'date_of_birth': ['1990-05-15'],
        'company_id': ['123'],
        'disc_profile': ['D'],
        'disc_sales': ['High Performer'],
        'disc_communication': ['Direct and Brief'],
        'leadership_style': ['Transformational'],
        'team_dynamics': ['Collaborative'],
        'conflict_resolution': ['Mediation-Oriented'],
        'customer_service_approach': ['Empathetic Listening'],
        'decision_making_style': ['Data-Driven'],
        'workplace_behavior': ['Proactive and Detail-Oriented'],
        'hiring_and_recruitment': ['Culture-First'],
        'coaching_and_development': ['Growth Mindset Focused'],
        'industry': ['Technology'],
        'position': ['Senior Manager'],
        'company_size': ['500-1000'],
        'website': ['https://example.com'],
        'assessment_date': ['2024-01-15']
    }
    
    return pd.DataFrame(sample_data)

def convert_gsheets_url(url):
    """Convert Google Sheets sharing URL to CSV export URL"""
    if 'docs.google.com/spreadsheets' in url:
        # Extract the spreadsheet ID from the URL
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
        if match:
            spreadsheet_id = match.group(1)
            return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
    return url

def load_data_from_url(url):
    """Load CSV data from URL"""
    try:
        # Convert Google Sheets URL if needed
        csv_url = convert_gsheets_url(url)
        
        # Read CSV data
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Parse CSV
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        return df, None
    except Exception as e:
        return None, str(e)

def configure_aggrid(df):
    """Configure AgGrid options with enhanced styling"""
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Enable features
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    gb.configure_default_column(
        groupable=True, 
        value=True, 
        enableRowGroup=True, 
        aggFunc='sum', 
        editable=False,
        filter=True,
        sortable=True,
        resizable=True
    )
    
    # Configure specific columns with better formatting
    column_configs = {
        # Personal Information - Pinned to left
        'prefix': {'width': 80, 'pinned': 'left'},
        'first_name': {'width': 120, 'pinned': 'left'},
        'last_name': {'width': 120, 'pinned': 'left'},
        'full_name': {'width': 150, 'pinned': 'left'},
        'email': {'width': 200},
        'phone': {'width': 150},
        'timezone': {'width': 150},
        
        # Address Information
        'address_line_1': {'width': 150},
        'address_line_2': {'width': 120},
        'city': {'width': 120},
        'state': {'width': 80},
        'postal_code': {'width': 100},
        'country': {'width': 120},
        'ip': {'width': 120},
        
        # DISC Profile Information - Enhanced styling
        'disc_profile': {'width': 100, 'cellStyle': {'backgroundColor': '#e3f2fd'}},
        'disc_sales': {'width': 150, 'wrapText': True, 'autoHeight': True},
        'disc_communication': {'width': 150, 'wrapText': True, 'autoHeight': True},
        'leadership_style': {'width': 150, 'wrapText': True, 'autoHeight': True},
        'team_dynamics': {'width': 150, 'wrapText': True, 'autoHeight': True},
        'conflict_resolution': {'width': 180, 'wrapText': True, 'autoHeight': True},
        'customer_service_approach': {'width': 180, 'wrapText': True, 'autoHeight': True},
        'decision_making_style': {'width': 150, 'wrapText': True, 'autoHeight': True},
        'workplace_behavior': {'width': 200, 'wrapText': True, 'autoHeight': True},
        'hiring_and_recruitment': {'width': 150, 'wrapText': True, 'autoHeight': True},
        'coaching_and_development': {'width': 200, 'wrapText': True, 'autoHeight': True},
        
        # Company Information
        'company_id': {'width': 100},
        'industry': {'width': 120},
        'position': {'width': 150},
        'company_size': {'width': 120},
        'website': {'width': 180},
        
        # Dates
        'date_of_birth': {'width': 120},
        'assessment_date': {'width': 120},
        'source': {'width': 120}
    }
    
    # Apply column configurations
    for col, config in column_configs.items():
        if col in df.columns:
            gb.configure_column(
                col, 
                width=config.get('width', 100),
                pinned=config.get('pinned', None),
                wrapText=config.get('wrapText', False),
                autoHeight=config.get('autoHeight', False),
                cellStyle=config.get('cellStyle', {})
            )
    
    gridOptions = gb.build()
    return gridOptions

def display_data_summary(df):
    """Display comprehensive data summary"""
    st.subheader("📊 Data Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        unique_companies = df['company_id'].nunique() if 'company_id' in df.columns else 0
        st.metric("Unique Companies", unique_companies)
    with col4:
        disc_profiles = df['disc_profile'].nunique() if 'disc_profile' in df.columns else 0
        st.metric("DISC Profiles", disc_profiles)
    
    # DISC Profile Distribution
    if 'disc_profile' in df.columns:
        st.subheader("🎯 DISC Profile Distribution")
        disc_counts = df['disc_profile'].value_counts()
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(disc_counts.reset_index())
        with col2:
            st.bar_chart(disc_counts)

def main():
    st.set_page_config(
        page_title="Live CSV Data Viewer - DISC Profiles",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Live CSV Data Viewer - DISC Profiles & Personnel Data")
    st.markdown("*Optimized for personnel data with DISC assessments and company information*")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data source selection
        data_source = st.radio(
            "Select Data Source:",
            ["Sample Data", "Google Sheets URL", "CSV URL"],
            help="Choose your data source"
        )
        
        if data_source != "Sample Data":
            url_input = st.text_input(
                "Enter URL:",
                placeholder="https://docs.google.com/spreadsheets/d/your-sheet-id/edit#gid=0",
                help="Paste your Google Sheets sharing URL or direct CSV URL"
            )
        else:
            url_input = None
        
        # Display options
        st.subheader("📋 Display Options")
        show_summary = st.checkbox("Show Data Summary", value=True)
        show_column_info = st.checkbox("Show Column Information", value=False)
        
        # Auto-refresh option
        st.subheader("🔄 Refresh Settings")
        auto_refresh = st.checkbox("Auto-refresh data", value=False)
        if auto_refresh:
            refresh_interval = st.slider("Refresh interval (seconds)", 10, 300, 60)
        
        # Manual refresh button
        refresh_button = st.button("🔄 Refresh Data", type="primary")
    
    # Load data based on source
    df = None
    error = None
    
    if data_source == "Sample Data":
        df = get_sample_data()
        st.info("📝 Displaying sample data with the provided example record")
    elif url_input:
        with st.spinner("Loading data from URL..."):
            df, error = load_data_from_url(url_input)
    
    # Display data or error
    if error:
        st.error(f"❌ Error loading data: {error}")
        st.info("💡 Make sure your Google Sheets is publicly accessible or use a direct CSV URL")
        
        # Show sample data as fallback
        st.markdown("---")
        st.info("📝 Showing sample data instead:")
        df = get_sample_data()
    
    if df is not None and not df.empty:
        # Display data summary
        if show_summary:
            display_data_summary(df)
            st.markdown("---")
        
        # Display column information
        if show_column_info:
            with st.expander("📋 Column Information"):
                st.write("**Available Columns:**")
                
                # Group columns by category
                personal_cols = ['prefix', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'timezone']
                address_cols = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'ip']
                disc_cols = [col for col in df.columns if 'disc' in col.lower() or col in ['leadership_style', 'team_dynamics', 'conflict_resolution', 'customer_service_approach', 'decision_making_style', 'workplace_behavior', 'hiring_and_recruitment', 'coaching_and_development']]
                company_cols = ['company_id', 'industry', 'position', 'company_size', 'website']
                other_cols = ['source', 'date_of_birth', 'assessment_date']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**👤 Personal Information:**")
                    for col in personal_cols:
                        if col in df.columns:
                            st.write(f"• {col}")
                    
                    st.write("**🏠 Address Information:**")
                    for col in address_cols:
                        if col in df.columns:
                            st.write(f"• {col}")
                
                with col2:
                    st.write("**🎯 DISC Profile & Behavior:**")
                    for col in disc_cols:
                        if col in df.columns:
                            st.write(f"• {col}")
                    
                    st.write("**🏢 Company Information:**")
                    for col in company_cols:
                        if col in df.columns:
                            st.write(f"• {col}")
                    
                    st.write("**📅 Other Information:**")
                    for col in other_cols:
                        if col in df.columns:
                            st.write(f"• {col}")
        
        # Configure and display AgGrid
        st.subheader("📊 Interactive Data Table")
        
        try:
            gridOptions = configure_aggrid(df)
            
            grid_response = AgGrid(
                df,
                gridOptions=gridOptions,
                data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                update_mode=GridUpdateMode.MODEL_CHANGED,
                fit_columns_on_grid_load=False,
                theme='streamlit',
                enable_enterprise_modules=True,
                height=600,
                width='100%',
                reload_data=refresh_button or auto_refresh
            )
            
            # Display selection info
            if grid_response['selected_rows'] is not None and len(grid_response['selected_rows']) > 0:
                st.subheader("✅ Selected Records")
                selected_df = pd.DataFrame(grid_response['selected_rows'])
                st.dataframe(selected_df, use_container_width=True)
                
                # Download selected data
                csv = selected_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Selected Data as CSV",
                    data=csv,
                    file_name="selected_personnel_data.csv",
                    mime="text/csv"
                )
            
            # Download all data
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                csv_all = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Data as CSV",
                    data=csv_all,
                    file_name="personnel_data.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Export filtered data
                filtered_df = pd.DataFrame(grid_response['data'])
                csv_filtered = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv_filtered,
                    file_name="filtered_personnel_data.csv",
                    mime="text/csv"
                )
            
        except Exception as e:
            st.error(f"❌ Error displaying data: {str(e)}")
            st.dataframe(df, use_container_width=True)
    
    elif data_source != "Sample Data":
        # Instructions
        st.info("👆 Please enter a Google Sheets URL or CSV URL in the sidebar to get started.")
        
        st.markdown("""
        ### 🚀 How to use:
        
        1. **Sample Data**: View the example with your provided data structure
        2. **Google Sheets URL**: Share your Google Sheet publicly and paste the URL
        3. **Direct CSV URL**: Use any direct CSV file URL
        
        ### ✨ Features:
        - 📊 Interactive data table with sorting, filtering, and grouping
        - 🎯 DISC profile analysis and visualization
        - 🔍 Advanced search and column filtering
        - 📱 Responsive design optimized for personnel data
        - 📥 Download filtered, selected, or all data
        - 🔄 Auto-refresh capability for live data
        - 📋 Multi-row selection with checkboxes
        - 🏢 Company and personnel analytics
        
        ### 📋 Optimized for:
        - **Personal Information**: Names, contact details, addresses
        - **DISC Assessments**: Complete behavioral profiles and analysis
        - **Company Data**: Industry, position, company size information
        - **Assessment Tracking**: Dates, sources, and progress monitoring
        """)
    
    # Auto-refresh functionality
    if auto_refresh and (url_input or data_source == "Sample Data"):
        import time
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
