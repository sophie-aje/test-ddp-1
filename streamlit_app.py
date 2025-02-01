import pandas as pd
import streamlit as st
import time
import requests
import io

# Add a header for the app
st.title("Ngee Ann Real-Time Bus Arrival Tracker")
st.markdown(""" Welcome to the Ngee Ann Polytechnic Real-Time Bus Arrival Tracker! 
This app provides real-time bus arrival information for buses serving Ngee Ann Polytechnic. 
Stay updated and plan your journey with ease. """)

# Load data without caching
def load_data():
    # Use the raw GitHub URL for the file
    github_raw_url = "https://raw.githubusercontent.com/sophie-aje/test-ddp-1/main/path/in/repo/DDP_OUTPUT.xlsx"
    response = requests.get(github_raw_url)
    response.raise_for_status()  # Check for errors
    
    # Load the Excel file from the response content
    file_like = io.BytesIO(response.content)
    sheets = ["NextBus1", "NextBus2", "NextBus3"]
    data = pd.concat(
        [pd.read_excel(file_like, sheet_name=sheet, header=0, usecols=None) for sheet in sheets],
        ignore_index=True
    )
    data.columns = data.columns.str.strip()
    return data
    
# Load data
data = load_data()

# Clean column names
data.columns = data.columns.str.strip()

# Get unique bus stop descriptions instead of codes
bus_stops = data[["BusStopCode", "BusStopDescription"]].drop_duplicates()

# Create a dictionary to map BusStopCode to its Description
bus_stop_dict = dict(zip(bus_stops["BusStopCode"], bus_stops["BusStopDescription"]))

# Create Streamlit tabs using bus stop descriptions
tabs = st.tabs([bus_stop_dict[code] for code in bus_stop_dict])

# Load Icons for Different Attributes
ICON_BASE = "https://img.icons8.com/ios-filled/50"

BUS_TYPE_ICONS = {
    "SD": f"{ICON_BASE}/4caf50/bus.png",  # Single Deck (Green)
    "DD": f"{ICON_BASE}/3b82f6/double-decker-bus.png",  # Double Deck (Blue)
    "BD": f"https://static.thenounproject.com/png/336478-200.png"  # Bendy Bus (Red)
}

WHEELCHAIR_ICONS = {
    "WAB": f"{ICON_BASE}/4caf50/wheelchair.png",  # Wheelchair Accessible (Green)
    "NO": f"{ICON_BASE}/fa314a/wheelchair.png"  # Not Accessible (Red)
}

# Operator Icons
OPERATOR_ICONS = {
    "SBST": "https://media.licdn.com/dms/image/v2/C560BAQH0a2_Cv6Eldw/company-logo_200_200/company-logo_200_200/0/1630655352507/sbs_transit_ltd_logo?e=2147483647&v=beta&t=72jKzOPN6m4ZH1U5SQdtWrlC_Wbcs3iUS95DIOw2nxI",  # SBS Transit logo
    "SMRT": "https://upload.wikimedia.org/wikipedia/en/b/be/SMRT_Corporation_logo.png?20160902060638",  # SMRT Corporation logo
    "TTS": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/TowerTransitLogo.svg/615px-TowerTransitLogo.svg.png?20240208135732",  # Tower Transit Singapore logo
    "GAS": "data:image/png;base64,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",  # Go Ahead Singapore logo
}
# Process each bus stop tab
for i, code in enumerate(bus_stop_dict.keys()):
    with tabs[i]:
        # Filter data for each bus stop code
        filtered_data = data[data["BusStopCode"] == code]

        # Add search bar for bus service number within the bus stop
        bus_service_query = st.text_input(f"🔍 Search for a bus service number at {bus_stop_dict[code]}:", key=f"bus_search_{code}").strip()

        if bus_service_query:
            filtered_data = filtered_data[filtered_data["BusNo"].astype(str).str.contains(bus_service_query, case=False, na=False)]

        if filtered_data.empty:
            st.warning(f"No buses found for {bus_stop_dict[code]}.")
        else:
            # Group by bus number and display header
            for bus_no, bus_data in filtered_data.groupby("BusNo"):
                destination = bus_data["DestinationDescription"].iloc[0]

                # Bus header with icon and destination
                st.markdown(f"""
                <div class="bus-header">
                    <img src="https://img.icons8.com/ios-filled/50/000000/bus.png" alt="bus-icon">
                    Bus {bus_no} - {destination}
                </div>
                """, unsafe_allow_html=True)

                                # Custom CSS for styling
                st.markdown("""
                <style>
                    .arrival-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 20px;
                        margin-top: 10px;
                    }
                    .arrival-card {
                        background-color: white;
                        border-radius: 10px;
                        padding: 20px;
                        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                        text-align: center;
                        width: 200px;
                    }
                    .arrival-card h4 {
                        margin: 0;
                        font-size: 16px;
                        font-weight: bold;
                        color: #555;
                    }
                    .minutes {
                        font-size: 30px;
                        font-weight: bold;
                        margin: 10px 0;
                    }
                    .sea { color: #4caf50; }  /* Green */
                    .sda { color: #ffcc00; }  /* Yellow */
                    .lsd { color: #ff3b30; }  /* Red */
                    .icon-container {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                        margin-top: 10px;
                    }
                    .expander {
                        max-width: 600px;
                        margin: auto;
                    }
                </style>
                """, unsafe_allow_html=True)



                # Sort by NextBusGroup to ensure correct order
                bus_data = bus_data.sort_values("NextBusGroup")
                # Initialize session state for auto-refresh 
                if "last_refresh" not in st.session_state: 
                    st.session_state.last_refresh = time.time() 
                
                # Button to refresh the app
                if st.button("🔄 Refresh Data"):
                    st.cache_data.clear()  # Clear cache so the latest file is loaded
                    st.rerun()  # Fully refresh the app

                    # Create a horizontal layout for arrival times
                cols = st.columns(len(bus_data))  # Create columns for each arrival
                for idx, (_, row) in enumerate(bus_data.iterrows()):
                    with cols[idx]:
                        # Assign color based on Load
                        if row["Load"] == "SEA":
                            minutes_class = "sea"
                        elif row["Load"] == "SDA":
                            minutes_class = "sda"
                        elif row["Load"] == "LSD":
                            minutes_class = "lsd"
                        else:
                            minutes_class = "sea"  # Default to green

                        # Check if MinutesToArrival is 0 and replace with "Arr"
                        minutes_to_arrival = "Arr" if row["MinutesToArrival"] == 0 else f"{row['MinutesToArrival']} min"

                        # Determine icons
                        wheelchair_icon = WHEELCHAIR_ICONS["WAB"] if row["WheelchairAccessible"] == "WAB" else WHEELCHAIR_ICONS["NO"]
                        bus_type_icon = BUS_TYPE_ICONS.get(row["TypeOfBus"], f"{ICON_BASE}/gray/unknown.png")  # Default unknown
                        operator_icon = OPERATOR_ICONS.get(row["Operator"], f"{ICON_BASE}/gray/unknown.png")  # Default unknown

                        # Format date and time
                        # Handle null EstimatedTimeOfArrival
                        arrival_time = row["EstimatedTimeOfArrival"]
                        if pd.isna(arrival_time) or arrival_time is pd.NaT:
                            formatted_date = "Time data unavailable"
                            formatted_time = ""
                        else:
                            formatted_date = arrival_time.strftime('%d/%m/%Y')  # Date with slashes
                            formatted_time = arrival_time.strftime('%H:%M:%S')  # Time with seconds

                        # Render arrival card
                        st.markdown(f"""
                        <div class="arrival-card">
                            <h4>{row['NextBusGroup']}</h4>
                            <div class="minutes {minutes_class}">{minutes_to_arrival}</div>
                            <p><b>Arrival Time:</b> 
                                <span style="font-size: 15px; color: #777;">{formatted_date}</span>
                                <span style="font-size: 18px; font-weight: bold;">{formatted_time}</span>
                            </p>
                            <div class="icon-container">
                                <img src="{bus_type_icon}" alt="bus-type-icon" width="24px">
                                <img src="{wheelchair_icon}" alt="wheelchair-icon" width="24px">
                                <img src="{operator_icon}" alt="operator-icon" width=80px">
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                            
                        # Check if the bus arrival time is monitored or based on the schedule
                        is_monitored_value = row["Monitored"]
                        if is_monitored_value == 1:
                            is_monitored_text = "✅ Based on Location"
                        elif is_monitored_value == 0:
                            is_monitored_text = "📅 Based on operator schedule"
                        else:
                            is_monitored_text = "❓ Unknown status"
                        # Dropdown for additional information
                        with st.expander("More Info", expanded=False):
                            st.write(f"**Operator:** {row['Operator']}")
                            st.write(f"**Load Status:** {row['Load']}")
                            st.write(f"**Bus Type:** {row['TypeOfBus']}")
                            st.write(f"**Wheelchair Accessible:** {row['WheelchairAccessible']}")
                            # Smaller text for "Is Monitored"
                            st.markdown(
                                f'<p style="font-size: 15px;"><b>Is Monitored:</b> {is_monitored_text}</p>',
                                unsafe_allow_html=True
                            )
