from logging import disable
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import DISABLED, E, NORMAL
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import math as math
import pandas as pd
from numpy.core.einsumfunc import einsum

class App():
    def __init__(self, master):

        self.master = master

        #Main script
        self.frame_bg1 = tk.Frame(master, bg="#DCE4E6")
        self.frame_bg1.grid(column = 0, row = 0,sticky = "NW")

        self.frame_bg2 = tk.Frame(master, bg="#DCE4E6")
        self.frame_bg2.grid(column = 1, row = 0,sticky = "NW")

        self.frame_bg3 = tk.Frame(master, bg="#DCE4E6")
        self.frame_bg3.grid(column = 2, row = 0,sticky = "NW")

        self.frame_open = tk.Frame(self.frame_bg1, bg="#DCE4E6")
        self.frame_open.grid(column = 0, row = 0, sticky = "NW", )

        self.frame_slider_y = tk.Frame(self.frame_bg2, bg="#DCE4E6")
        self.frame_slider_y.grid(column = 1, row = 0, sticky = "NW")

        self.frame_canvas1 = tk.Frame(self.frame_bg3, bg="#DCE4E6")
        self.frame_canvas1.grid(column = 2, row = 0, sticky = "NW", pady=5, columnspan=2)

        self.frame_slider_x = tk.Frame(self.frame_bg3, bg="#DCE4E6")
        self.frame_slider_x.grid(column = 2, row = 1, sticky = "NW",columnspan=2)

        self.frame_set_butt = tk.Frame(self.frame_bg2, bg="#DCE4E6")
        self.frame_set_butt.grid(column = 1, row = 1,sticky = "NW")

        self.frame_slope_butt = tk.Frame(self.frame_bg2, bg="#DCE4E6")
        self.frame_slope_butt.grid(column = 1, row = 2,sticky = "NW",pady=100)

        self.frame_canvas2 = tk.Frame(self.frame_bg3, bg="#DCE4E6")
        self.frame_canvas2.grid(column = 2, row = 2, sticky = "NW", pady=5, padx= 5, columnspan=2)

        self.frame_dimensions = tk.Frame(self.frame_bg1, bg="#DCE4E6")
        self.frame_dimensions.grid(column = 0, row = 1, sticky = "NW",pady = 15)

        self.frame_test_samp = tk.Frame(self.frame_bg1, bg="#DCE4E6")
        self.frame_test_samp.grid(column = 0, row = 2, sticky = "NW",pady = 15)

        self.frame_results = tk.Frame(self.frame_bg1, bg="#cad6dc", highlightthickness = 2, highlightbackground = "#5e5f5d")
        self.frame_results.grid(column = 0, row = 3, sticky = "NW" ,pady = 60, padx = 125)



        # Plot 1 
        self.fig_1 = Figure(figsize=(5,2.75), dpi=100, tight_layout = True)
        self.ax1 = self.fig_1.add_subplot(111)
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.ax1.plot([],[])       
    
        self.canvas1 = FigureCanvasTkAgg(self.fig_1, self.frame_canvas1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0,column=1,padx=5)

        # File Open button 
        self.open_bt = tk.Button(self.frame_open, text = "Open", height = 2, width = 4, command=self.load_file)
        self.open_bt.grid(column = 0, row = 0, padx=5, pady = 10, sticky = "W")

        # File name textbox
        self.file_box = tk.Text(self.frame_open, height = 2, width = 50)
        self.file_box.grid(column = 1, row = 0, sticky = "W", padx = 10, pady = 10)
        self.file_box.config(font=("Arial", 10),)

        # File Plot button 
        self.plot_bt = tk.Button(self.frame_open, text = "Plot", height = 2, width = 4, command= self.plot_origin)
        self.plot_bt.grid(column = 2, row = 0, padx=2, pady = 10, sticky = "E")

        # File Clear button 
        self.plot_bt = tk.Button(self.frame_open, text = "Clear", height = 2, width = 4, command=self.clear_plot)
        self.plot_bt.grid(column = 3, row = 0, padx=2, pady = 10, sticky = "W")

        #slider_y
        self.move_avg_y = tk.DoubleVar()
        self.slider_y = tk.Scale(self.frame_slider_y, from_=0, to=100, length=275, orient='vertical', command= self.slider_changed_data)
        self.slider_y.grid(column = 0, row = 0, padx= 5)     
        
        #slider_x
        self.slider_x = tk.Scale(self.frame_slider_x, from_=0, to=100, length=500, orient='horizontal', command= self.slider_changed_data)
        self.slider_x.grid(column = 0, row = 0, padx= 5, pady =20) 

        #Set and resetbutton
        self.label_mvag = tk.Label(self.frame_set_butt, text = "Moving Avg.", bg="#DCE4E6")
        self.label_mvag.grid(column = 0, row = 0, pady = 1)

        self.set_bt = tk.Button(self.frame_set_butt, text = "Set", width = 8, command = self.set_plot)
        self.set_bt.grid(column = 0, row = 1, pady = 1)

        self.reset_bt = tk.Button(self.frame_set_butt, text = "Reset", width = 8, command = self.slider_reset)
        self.reset_bt.grid(column = 0, row = 2, pady = 1)


        #plot slope button 
        self.slope_bt = tk.Button(self.frame_slope_butt, text = "Plot Slope", width = 8, command = self.plot_slope)
        self.slope_bt.grid(column = 0, row = 0, pady = 1)
        
        self.slope_clear = tk.Button(self.frame_slope_butt, text = "Clear", width = 8, command = self.clear_slope)
        self.slope_clear.grid(column = 0, row = 1, pady= 50 )
  

        # Plot 2 
        self.fig_2 = Figure(figsize=(5, 2.75), dpi=100, tight_layout = True)
        self.ax2 = self.fig_2.add_subplot(111)
        self.ax2.set_xlabel("Displacement (mm)")
        self.ax2.set_ylabel("Force (N)")
        self.ax2.plot([],[])
       
        self.canvas2 = FigureCanvasTkAgg(self.fig_2,self.frame_canvas2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=2,column=1,padx=5, pady = 5)

        # Sample Dimensions 
        self.label_sample = tk.Label(self.frame_dimensions, text = "Sample Dimensions")
        self.label_sample.grid(column = 0, row = 1, sticky = "W", padx=10, pady = 2)
        self.label_sample.config(font=('Arial',10,'bold','underline'),bg="#DCE4E6")

        # Height
        self.label_height = tk.Label(self.frame_dimensions, text = "Height (mm)")
        self.label_height.grid(column = 0, row = 2, padx = 10, pady = 2, sticky = "W")
        self.label_height.config(font = ("Arial", 10),bg="#DCE4E6")
        self.height_box = tk.Text(self.frame_dimensions, height = 1, width = 10)
        self.height_box.grid(column = 1, row = 2, padx = 10, pady = 2, sticky = "W")
        self.height_box.config(font = ("Arial", 10))

        # Width 
        self.label_width = tk.Label(self.frame_dimensions, text = "Width (mm)")
        self.label_width.grid(column = 0, row = 3, padx = 10, pady = 2, sticky = "W")
        self.label_width.config(font = ("Arial", 10), bg="#DCE4E6")
        self.width_box = tk.Text(self.frame_dimensions, height = 1, width = 10)
        self.width_box.grid(column = 1, row = 3, padx = 10, pady = 2, sticky = "W")
        self.width_box.config(font = ("Arial", 10), )

        # Diameter
        self.label_di = tk.Label(self.frame_dimensions, text = "Diameter (mm)")
        self.label_di.grid(column = 0, row = 4, padx = 10, pady = 2, sticky = "W")
        self.label_di.config(font = ("Arial", 10), bg="#DCE4E6")
        self.di_box = tk.Text(self.frame_dimensions, height = 1, width = 10, state= NORMAL)
        self.di_box.grid(column = 1, row = 4, padx = 10, pady = 2, sticky = "W")
        self.di_box.config(font = ("Arial", 10))

        # Cross Section Label
        self.cross_sec = tk.Label(self.frame_dimensions, text = "Cross Section")
        self.cross_sec.grid(column = 2, row = 1, sticky = "W", padx=10)
        self.cross_sec.config(font=('Arial',10,'bold','underline'),bg="#DCE4E6")

        # Cross sectional Radio buttons
        self.area_option = tk.IntVar() 
        self.rad_butt_3 = tk.Radiobutton(self.frame_dimensions, text= "Square", variable= self.area_option, value = 1)
        self.rad_butt_3.grid(column=2, row = 2)
        self.rad_butt_3.config(font = ("Arial", 10), bg="#DCE4E6")
        self.rad_butt_4 = tk.Radiobutton(self.frame_dimensions, text= "Circular", variable= self.area_option, value = 2)
        self.rad_butt_4.grid(column=2, row = 3, pady = 5)
        self.rad_butt_4.config(font = ("Arial", 10),bg="#DCE4E6")

        
        # Radio Buttons for test and sample geometry
        # Test Label 
        self.test_label = tk.Label(self.frame_test_samp, text = "Test Type")
        self.test_label.grid(column = 0, row = 0, sticky = "W", padx=10, pady = 10)
        self.test_label.config(font=('Arial',10,'bold','underline'),bg="#DCE4E6")

        # radio buttons
        self.test_option = tk.IntVar() 
        self.rad_butt_1 = tk.Radiobutton(self.frame_test_samp, text= "3-Point", variable= self.test_option, value = 1)
        self.rad_butt_1.grid(column=0, row = 1, pady = 5)
        self.rad_butt_1.config(font = ("Arial", 10),bg="#DCE4E6")
        self.rad_butt_2 = tk.Radiobutton(self.frame_test_samp, text= "4-Point", variable= self.test_option, value = 2)
        self.rad_butt_2.grid(column=0, row = 2, pady = 5)
        self.rad_butt_2.config(font = ("Arial", 10), bg="#DCE4E6")

        # Span Entry 
        self.label_span = tk.Label(self.frame_test_samp, text = "Span Dimensions")
        self.label_span.grid(column= 1, row = 0, sticky = "W", padx = 25, pady = 5)
        self.label_span.config(font=('Arial',10,'bold','underline'),bg="#DCE4E6")

        # Span Top
        self.spantop_lab = tk.Label(self.frame_test_samp, text = "Top Span (mm)")
        self.spantop_lab.grid(column = 1, row = 1, padx = 25, pady = 2, sticky = "W")
        self.spantop_lab.config(font = ("Arial", 10),bg="#DCE4E6")
        self.spantop_box = tk.Text(self.frame_test_samp, height = 1, width = 10)
        self.spantop_box.grid(column = 2, row = 1, padx = 10, pady = 2, sticky = "W")
        self.spantop_box.insert(tk.END, "25.4")
        self.spantop_box.config(font = ("Arial", 10))

        # Span Bottom
        self.spanbot_lab = tk.Label(self.frame_test_samp, text = "Bottom Span (mm)")
        self.spanbot_lab.grid(column = 1, row = 2, padx = 25, pady = 2, sticky = "W")
        self.spanbot_lab.config(font = ("Arial", 10),bg="#DCE4E6")
        self.spanbot_box = tk.Text(self.frame_test_samp, height = 1, width = 10)
        self.spanbot_box.grid(column = 2, row = 2, padx = 10, pady = 2, sticky = "W")
        self.spanbot_box.insert(tk.END, "50.8")
        self.spanbot_box.config(font = ("Arial", 10))
        
        # Calculate button
        self.plot_bt = tk.Button(self.frame_test_samp, text = "Calculate", height = 2, width = 10, command= lambda: [self.smoa_calc(), self.calc_e(),self.flex_stren()])
        self.plot_bt.grid(column = 2, row = 3, padx=2, pady = 10, sticky = "W")


        # Results 
        self.label_results = tk.Label(self.frame_results, text = "Results")
        self.label_results.grid(column= 0, row = 0, sticky = "NW", padx = 10, pady = 10)
        self.label_results.config(font=('Arial',18,'bold','underline'), bg="#cad6dc")

        # Results EI
        self.ei_lab = tk.Label(self.frame_results, text = "EI (N m²) = ")
        self.ei_lab.grid(column = 0, row = 1, padx = 25, pady = 10, sticky = "W")
        self.ei_lab.config(font = ("Arial", 18),bg="#cad6dc")
        self.ei_box = tk.Text(self.frame_results, height = 1, width = 10)
        self.ei_box.grid(column = 1, row = 1, padx = 5, pady = 10, sticky = "W")
        self.ei_box.config(font = ("Arial", 18,"bold"))

        # Results E
        self.e_lab = tk.Label(self.frame_results, text = "E (GPa) = ")
        self.e_lab.grid(column = 0, row = 2, padx = 25, pady = 10, sticky = "W")
        self.e_lab.config(font = ("Arial", 18),bg="#cad6dc")
        self.e_box = tk.Text(self.frame_results, height = 1, width = 10)
        self.e_box.grid(column = 1, row = 2, padx = 5, pady = 10, sticky = "W")
        self.e_box.config(font = ("Arial", 18, "bold"))

        # Results 
        self.flex_str_lab = tk.Label(self.frame_results, text = "Flexural Strength = ")
        self.flex_str_lab.grid(column = 0, row = 3, padx = 25, pady = 2, sticky = "W")
        self.flex_str_lab.config(font = ("Arial", 18), bg="#cad6dc")
        self.flex_box = tk.Text(self.frame_results, height = 1, width = 10)
        self.flex_box.grid(column = 1, row = 3, padx = 5, pady = 10, sticky = "W")
        self.flex_box.config(font = ("Arial", 18, "bold"))

        
      

    ''' Below the code contains the methods used for each of the interactive elements of the GUI
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

    # Method for opening file
    def load_file(self):
        global fname
        fname = filedialog.askopenfilename(filetypes=(("Labview files", "*.lvm"),
                                           ("Text files", "*.txt"),
                                           ("All files", "*.*") ))
        
        # File Open label 
        self.file_box.delete(1.0, tk.END)
        self.file_box.insert(tk.END, fname)

        # Extract data from read file 
        global df
        df = pd.read_csv(fname, sep="\t",header=None)
    
    # Method for plotting the sample data
    def plot_origin (self):
        # Plot the data 
        self.ax1.plot(df[1], df[2], linestyle = "solid")
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.canvas1.draw()

    # clear plot button function 
    def clear_plot(self):
        self.fig_1 = Figure(figsize=(5,3), dpi=100, tight_layout = True)
        self.ax1 = self.fig_1.add_subplot(111)
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.ax1.plot([],[])       
    
        self.canvas1 = FigureCanvasTkAgg(self.fig_1,self.frame_canvas1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0,column=1,padx=5, pady = 5)

    def slider_reset(self):
        #reset and activate sliders 
        self.slider_y['state'] = 'active'
        self.slider_x['state'] = 'active'
        self.slider_y.set(0)
        self.slider_x.set(0)

        #clear the plot 
        self.fig_1 = Figure(figsize=(5,3), dpi=100, tight_layout = True)
        self.ax1 = self.fig_1.add_subplot(111)
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.ax1.plot([],[])       
    
        self.canvas1 = FigureCanvasTkAgg(self.fig_1,self.frame_canvas1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0,column=1,padx=5, pady = 5)

        # Plot the data 
        self.ax1.plot(df[1], df[2], linestyle = "solid", color="orange")
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.canvas1.draw()

        
    #Method for smoothing data using a moving average controled by sliders
    def slider_changed_data(self, value):
        #smooth x data to slider value 
        if self.slider_x.get() >= 1: 
            df[3] = df[1].rolling(window = self.slider_x.get(),min_periods= 1).mean()
        else:
            df[3]=df[1]

        #smooth x data to slider value 
        if self.slider_y.get() >= 1: 
            df[4] = df[2].rolling(window = self.slider_y.get(),min_periods= 1).mean()
        else:
            df[4] = df[2]        
       
        #plot data    
        self.fig_1 = Figure(figsize=(5,3), dpi=100, tight_layout = True)
        self.ax1 = self.fig_1.add_subplot(111)
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.ax1.plot([],[])       
    
        self.canvas1 = FigureCanvasTkAgg(self.fig_1,self.frame_canvas1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0,column=1,padx=5, pady = 5)
        
        self.ax1.plot(df[3], df[4], linestyle = "solid")
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.canvas1.draw()

    #Method for defining smoothed data 
    def set_plot (self):
        #deactivate sliders
        self.slider_y['state'] = 'disabled'
        self.slider_x['state'] = 'disabled'
        

        #set x and y
        global x
        global y
        x = df[3].to_numpy()
        y = df[4].to_numpy()

        # Plot the data 
        self.ax1.plot(x,y, linestyle = "solid")
        self.ax1.set_xlabel("Displacement (mm)")
        self.ax1.set_ylabel("Force (N)")
        self.canvas1.draw()

        #use span selector
        self.span = SpanSelector(self.ax1, self.onselect, 'horizontal', useblit=True,
                            rectprops=dict(alpha=0.2, facecolor='blue'), span_stays = True)
        
        return x, y 
        
    # One select widget
    def onselect(self, xmin, xmax):
        indmin, indmax = np.searchsorted(x, (xmin, xmax))
        indmax = min(len(x) - 1, indmax)

        # Placing ranges into variables 
        global x_range
        global y_range
        x_range = x[indmin:indmax]
        y_range = y[indmin:indmax]

        return  x_range, y_range


    # Method for plotting the slope
    def plot_slope(self):
        # Calculate the linear regression of selected area
        global m, b
        global r_squared

        # Regression line calculation (with displacmentin (mm))
        m, b = np.polyfit(x_range, y_range, 1) 
        global line_y
        line_y = []
        for line in range(len(x_range)):
            y_line = ((m * x_range[line]) + b)
            line_y.append(y_line)

        #calculate r_squared
        correlation_matrix = np.corrcoef(x_range, y_range)
        correlation_xy = correlation_matrix[0,1]
        r_squared = correlation_xy**2

        # Plot the data 
        self.ax2.plot(x_range, y_range, marker = ",", color='green', linestyle = "None")
        self.ax2.plot(x_range, line_y)
        self.ax2.set_xlim(x_range[0], x_range[-1])
        self.ax2.set_ylim(y_range.min(), y_range.max())
        self.ax2.set_xlabel("Displacement (mm)")
        self.ax2.set_ylabel("Force (N)")
        self.ax2.text(x_range[50], y_range.max() * 0.85, "R squared = " + str("{:.3}".format(r_squared)))
        self.ax2.text(x_range[50], y_range.max() * 0.75, "Slope = " + str("{:.4}".format(m)))
        
        self.canvas2.draw()

    # Method for resetting the second subplot after pressed clear button
    def clear_slope(self):
        self.fig_2 = Figure(figsize=(5, 2.75), dpi=100, tight_layout = True)
        self.ax2 = self.fig_2.add_subplot(111)
        self.ax2.set_xlabel("Displacement (mm)")
        self.ax2.set_ylabel("Force (N)")
        self.ax2.plot([],[])

        self.canvas2 = FigureCanvasTkAgg(self.fig_2,self.frame_canvas2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=2,column=1,padx=5, pady = 5)   

        # Method for calculating the second moment of area for the given cross sections    
    def smoa_calc(self):
        global smoa_area
        if self.area_option.get() == 1:
            h = float(self.height_box.get(1.0,1.9))/1000
            w = float(self.width_box.get(1.0,1.9))/1000
            smoa_area = (w * (h**3)/12)
            
        if self.area_option.get() == 2:
            r = (float(self.di_box.get(1.0,1.9))/2)/1000
            smoa_area = (math.pi * r**4)/4
           
        return smoa_area

    # Method for calculating the EI and E of a sample 
    def calc_e(self):
        global flex_rigid
        global mod
        # Get Spans from input boxes 
        a_span_len = float(self.spantop_box.get(1.0,1.9))/1000
        b_span_len = float(self.spanbot_box.get(1.0,1.9))/1000
        # Calculate "a"
        global a
        a = (b_span_len - a_span_len)/2
        # Calculate slope (m) in meters
        m_m = m*1000

        # Calculate EI and E for 3-point bend
        if self.test_option.get() == 1:
            flex_rigid = m_m * (b_span_len**3/48)
            mod = flex_rigid/smoa_area
            mod_GPa = mod/1e+9
            self.ei_box.insert(1.0, str('%6.2f' % (flex_rigid)))
            self.e_box.insert(1.0, str(str('{0:.2f}'.format(mod_GPa))))

        # Calculate EI and E for 4-point bend
        if self.test_option.get() == 2:
            flex_rigid = m_m *(a/48) * (3 * b_span_len**2 - 4 * a**2)
            mod = flex_rigid/smoa_area
            mod_GPa = mod/1e+9
            self.ei_box.insert(1.0, "")
            self.ei_box.insert(1.0, str(flex_rigid))
            self.e_box.insert(1.0, "")
            self.e_box.insert(1.0, str(mod_GPa))
        return mod, flex_rigid

    # Method for calculating flexural strength 
    def flex_stren(self):
        f_max = max(y)
        global flex_str
        flex_str = (f_max*a)/2
        self.flex_box.insert(1.0, str(flex_str))
        return flex_str

        

#Main script
root = tk.Tk()

root.config(bg="#DCE4E6")
root.title("Modlus Calculator")
root.geometry("1300x700")

app = App(root)

root.mainloop()
