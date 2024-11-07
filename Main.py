import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def plot_signal(binary_input, encoding):
    # Prepare the time vector for plotting
    time = []
    values = []
    last_polarity = -1  # Start with a negative polarity for AMI and Pseudoternary
    
    for i, bit in enumerate(binary_input):
        time.append(i)
        time.append(i + 1)  # Create a step for each bit
        
        if encoding == "NRZ-L":
            values.extend([int(bit)] * 2)  # Level is constant
        elif encoding == "NRZ-I":
            if i == 0:
                values.extend([int(bit)] * 2)
            else:
                values.extend([values[-1] ^ int(bit)] * 2)  # Toggle on '1'
        elif encoding == "Bipolar AMI":
            if bit == '1':
                # Alternate between +1 and -1 for each '1' bit
                last_polarity *= -1
                values.append(last_polarity)
            else:
                values.append(0)  # '0' stays at the middle level
            values.append(values[-1])
        elif encoding == "Pseudoternary":
            if bit == '0':
                # Alternate between +1 and -1 for each '0' bit
                last_polarity *= -1
                values.append(last_polarity)
            else:
                values.append(0)  # '1' stays at the middle level
            values.append(values[-1])
        elif encoding == "Manchester":
            if bit == '1':
                values.extend([1, 0])
            else:
                values.extend([0, 1])
        elif encoding == "Differential Manchester":
            if i == 0:
                values.extend([0, 1] if binary_input[0] == '1' else [1, 0])
            else:
                values.extend([1 - values[-1], values[-1]] if binary_input[i] == '1' else [values[-1], values[-1] ^ 1])

    # Plot the signal with bounds 0 and 1
    plt.step(time, values, where='post')
    plt.title(f"Digital Signal: {encoding} Encoding")
    plt.xlabel("Time (bits)")
    plt.ylabel("Signal Level")
    plt.ylim(-1.5, 1.5)  # Set y-axis bounds to show middle line at 0
    plt.xticks(range(len(binary_input) + 1))
    plt.yticks([-1, 0, 1])  # Show -1, 0, and 1 on y-axis
    plt.grid()

    # Draw the middle line at 0 for reference
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)

    # Annotate each bit value above the signal
    for i, bit in enumerate(binary_input):
        y = int(bit) if encoding != "Bipolar AMI" and encoding != "Pseudoternary" else values[2 * i]
        plt.text(i + 0.5, y + 0.1, bit, ha='center', va='bottom')

    plt.show()

def on_submit():
    user_input = entry.get()

    # Validate the input
    if len(user_input) > 10:
        messagebox.showerror("Error", "Input must be a maximum of 10 bits.")
        return
    if not all(bit in '01' for bit in user_input):
        messagebox.showerror("Error", "Input must be binary (only 0s and 1s).")
        return
    
    selected_option = radio_var.get()
    plot_signal(user_input, selected_option)

# Create the main window
root = tk.Tk()
root.title("Digital Signal Application")

# Create an entry widget
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create a variable to hold the selected radio button value
radio_var = tk.StringVar(value="NRZ-L")  # Default selection

# Create radio buttons
options = ["NRZ-L", "NRZ-I", "Bipolar AMI", "Pseudoternary", "Manchester", "Differential Manchester"]
for option in options:
    radio_button = tk.Radiobutton(root, text=option, variable=radio_var, value=option)
    radio_button.pack(anchor=tk.W)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
