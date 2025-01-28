import pandas as pd
import streamlit as st
import time
import requests
import io

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

# Initialize session state for auto-refresh 
if "last_refresh" not in st.session_state: 
    st.session_state.last_refresh = time.time() 
 
# Button to refresh the app
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()  # Clear cache so the latest file is loaded
    st.rerun()  # Fully refresh the app

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

# Operator Icons (Updated with alternative icons)
# Operator Icons (Updated with actual icons)
OPERATOR_ICONS = {
    "SBST": "https://media.licdn.com/dms/image/v2/C560BAQH0a2_Cv6Eldw/company-logo_200_200/company-logo_200_200/0/1630655352507/sbs_transit_ltd_logo?e=2147483647&v=beta&t=72jKzOPN6m4ZH1U5SQdtWrlC_Wbcs3iUS95DIOw2nxI",  # SBS Transit logo
    "SMRT": "https://upload.wikimedia.org/wikipedia/en/b/be/SMRT_Corporation_logo.png?20160902060638",  # SMRT Corporation logo
    "TTS": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/TowerTransitLogo.svg/615px-TowerTransitLogo.svg.png?20240208135732",  # Tower Transit Singapore logo
    "GAS": "data:image/png;base64,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",  # Go Ahead Singapore logo
}

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

# Use Bus Stop Description for tabs, but keep the code for filtering
tabs = st.tabs([bus_stop_dict[code] for code in bus_stop_dict])

# Process each bus stop tab
for i, code in enumerate(bus_stop_dict.keys()):
    with tabs[i]:
        # Filter data for each bus stop code
        filtered_data = data[data["BusStopCode"] == code]

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

                # Sort by NextBusGroup to ensure correct order
                bus_data = bus_data.sort_values("NextBusGroup")

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
                        arrival_time = row["EstimatedTimeOfArrival"]
                        formatted_date = arrival_time.strftime('%d/%m/%Y')  # Date with slashes
                        formatted_time = arrival_time.strftime('%H:%M:%S')  # Time with seconds

                        # Render arrival card
                        st.markdown(f"""
                        <div class="arrival-card">
                            <h4>{row['NextBusGroup']}</h4>
                            <div class="minutes {minutes_class}">{minutes_to_arrival}</div>
                            <p><b>Arrival Time:</b> 
                                <span style="font-size: 12px; color: #777;">{formatted_date}</span>
                                <span style="font-size: 18px; font-weight: bold;">{formatted_time}</span>
                            </p>
                            <div class="icon-container">
                                <img src="{bus_type_icon}" alt="bus-type-icon" width="24px">
                                <img src="{wheelchair_icon}" alt="wheelchair-icon" width="24px">
                                <img src="{operator_icon}" alt="operator-icon" width="100px">
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Dropdown for additional information
                        with st.expander("More Info", expanded=False):
                            st.write(f"**Operator:** {row['Operator']}")
                            st.write(f"**Load Status:** {row['Load']}")
                            st.write(f"**Bus Type:** {row['TypeOfBus']}")
                            st.write(f"**Wheelchair Accessible:** {row['WheelchairAccessible']}")
