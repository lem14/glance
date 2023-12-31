"""
# Welcome to Glance!
## alerts are binary, humans are not
Current floor plan: 
"""

# Function to create an interactive bubble
def interactive_bubble(label):
    if st.button(label):
        st.write(f"You clicked the bubble: {label}")




# Define the number of rows and columns in the grid
num_rows = 3
num_cols = 3

# Create the grid
for i in range(num_rows):
    col_list = []
    for j in range(num_cols):
        # Create a placeholder for the bubble label
        bubble_label = f"({i}, {j})"
        # Display the bubble
        col_list.append(interactive_bubble(bubble_label))
    
    # Display the row of bubbles
    st.write(col_list)

# To create a grid layout
# The number of rows and columns will be determined by the elements in the list

# Sample grid data
grid_data = [
    ['A', 'B', 'C'],
    ['D', 'E', 'F'],
    ['G', 'H', 'I']
]

# Display the grid layout
st.write('Grid Layout:')
#st.grid(grid_data)






# add toggle options
col1, col2, col3, col4 = st.columns(4)

with col1:
    warn_stats_on = st.toggle("View Warnings")

with col2:
    all_stats_on = st.toggle("View All Stats")

# build top row
col1, col2, col3, col4 = st.columns(4)

with col1:
    if all_stats_on:
        st.success('BP: 120/80, SpO2: 99', icon="✅")
    else:
        st.success('',icon="✅")

with col2:
    if all_stats_on:
        st.error('BP: 120/80, SpO2: 75', icon="🚨")
    else:
        st.error(" ", icon="🚨")

with col3:
   st.success('',icon="✅")

with col4:
   st.warning("", icon="⚠️")

# build side rows
col1, col2, col3, col4 = st.columns(4)

with col1:
   st.error(" ", icon="🚨")
   st.success('',icon="✅")
   st.warning("", icon="⚠️")

with col2:
   st.empty()

with col3:
   st.empty()

with col4:
   st.error(" ", icon="🚨")
   st.success('',icon="✅")
   st.success('',icon="✅")


import time

start_time = time.time()

def time_convert(sec):

    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    st.write("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

timer = st.button('press to start')

#if timer == True:
#    start_time = time.time()

#while timer == True:
#    end_time = time.time()
#    time_lapsed = end_time - start_time 
#    time_convert(time_lapsed)




# total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
# num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

# Point = namedtuple('Point', 'x y')
# data = []

# points_per_turn = total_points / num_turns

# for curr_point_num in range(total_points):
#     curr_turn, i = divmod(curr_point_num, points_per_turn)
#     angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#     radius = curr_point_num / total_points
#     x = radius * math.cos(angle)
#     y = radius * math.sin(angle)
#     data.append(Point(x, y))

# st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#     .mark_circle(color='#0068c9', opacity=0.5)
#     .encode(x='x:Q', y='y:Q'))