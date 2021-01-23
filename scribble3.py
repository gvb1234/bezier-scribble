#!/usr/bin/python3

#import pandas
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import cairo
import os
import gzip
import numpy
import sys
import math
import datetime



#os.environ['GDK_DEBUG'] = 'all'
#os.environ['GTK_DEBUG'] = 'all'
#os.environ['G_DEBUG'] = 'fatal-warnings'
#os.environ['G_MESSAGES_DEBUG'] = 'all'

# get the native window decorations
if os.name=='nt':
    os.environ['GTK_CSD'] = '0'
    import pkg_resources.py2_warn


#import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=sys.maxsize)

#!/usr/bin/env python3
from gi.repository import GdkPixbuf #,GLib

iconSize = Gtk.IconSize.LARGE_TOOLBAR


#settings = Gtk.Settings.get_default()
#settings.set_property("gtk-theme-name", "MS-Windows")
#settings.set_property("gtk-application-prefer-dark-theme", False)  # if you want use dark theme, set second arg to True

 
#for i in settings.list_properties():
#    print(i)
    

#%%

glade_string='''
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.20.4 -->
<interface>
  <requires lib="gtk+" version="3.4"/>
  <object class="GtkAdjustment" id="circleradiusadjustment">
    <property name="lower">15</property>
    <property name="upper">301</property>
    <property name="value">150</property>
    <property name="step_increment">1</property>
    <property name="page_increment">1</property>
    <property name="page_size">1</property>
    <signal name="value-changed" handler="slider_changed" swapped="no"/>
  </object>
  <object class="GtkImage" id="image1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="stock">gtk-open</property>
  </object>
  <object class="GtkImage" id="image2">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="stock">gtk-save</property>
  </object>
  <object class="GtkImage" id="image3">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="stock">gtk-save-as</property>
  </object>
  <object class="GtkImage" id="image4">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="stock">gtk-select-color</property>
  </object>
  <object class="GtkImage" id="image5">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="stock">gtk-preferences</property>
  </object>
  <object class="GtkAdjustment" id="linewidthadjustment">
    <property name="upper">101</property>
    <property name="value">32</property>
    <property name="step_increment">1</property>
    <property name="page_increment">10</property>
    <signal name="value-changed" handler="slider_changed" swapped="no"/>
  </object>
  <object class="GtkFileFilter" id="pdffilter">
    <mime-types>
      <mime-type>application/pdf</mime-type>
    </mime-types>
  </object>
  <object class="GtkFileFilter" id="pngfilter">
    <mime-types>
      <mime-type>image/png</mime-type>
    </mime-types>
  </object>
  <object class="GtkAdjustment" id="sectoropeningadjustment">
    <property name="upper">91</property>
    <property name="value">30</property>
    <property name="step_increment">10</property>
    <property name="page_increment">1</property>
    <property name="page_size">1</property>
    <signal name="value-changed" handler="slider_changed" swapped="no"/>
  </object>
  <object class="GtkWindow" id="window1">
    <property name="width_request">0</property>
    <property name="can_focus">False</property>
    <property name="hexpand">True</property>
    <property name="vexpand">True</property>
    <signal name="destroy" handler="Quit" swapped="no"/>
    <signal name="destroy-event" handler="Quit" swapped="no"/>
    <signal name="key-press-event" handler="KeyPressHandler" swapped="no"/>
    <child>
      <object class="GtkGrid" id="grid1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="margin_bottom">3</property>
        <property name="hexpand">True</property>
        <property name="vexpand">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkMenuBar" id="menubar">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="hexpand">True</property>
            <child>
              <object class="GtkMenuItem" id="FileMenu">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_File</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="FilemenuChild">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkImageMenuItem" id="OpenMenu">
                        <property name="label" translatable="yes">Open Image</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="image">image1</property>
                        <property name="use_stock">False</property>
                        <signal name="activate" handler="Open" swapped="no"/>
                        <accelerator key="o" signal="activate" modifiers="GDK_CONTROL_MASK"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="ExportMenu">
                        <property name="label" translatable="yes">Export</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="image">image2</property>
                        <property name="use_stock">False</property>
                        <signal name="activate" handler="Export" swapped="no"/>
                        <accelerator key="s" signal="activate" modifiers="GDK_CONTROL_MASK"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="ExportAsMenu">
                        <property name="label" translatable="yes">Export As</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="image">image3</property>
                        <property name="use_stock">False</property>
                        <signal name="activate" handler="ExportAs" swapped="no"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="separatormenuitem1">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="QuitMenu">
                        <property name="label">gtk-quit</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <signal name="activate" handler="Quit" swapped="no"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="SettingsMenu">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_Settings</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="SettingsMenuChild">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkCheckMenuItem" id="AutoScrollMenu">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label">AutoScroll</property>
                        <property name="use_underline">True</property>
                        <property name="active">True</property>
                        <signal name="toggled" handler="ToggleAutoScroll" swapped="no"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkCheckMenuItem" id="UseClosestPointMenu">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label">Use Closest Point</property>
                        <property name="use_underline">True</property>
                        <property name="active">True</property>
                        <signal name="toggled" handler="ToggleClosestPoint" swapped="no"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkCheckMenuItem" id="AutoAdjustPointsMenu">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label">Auto Adjust Points when moving</property>
                        <property name="active">True</property>
                        <signal name="toggled" handler="autoadjust_toggle" swapped="no"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkCheckMenuItem" id="UseLegacyColorPickerMenu">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label">Use Legacy Color Picker</property>
                        <property name="active">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="ConfigMenu">
                        <property name="label">Config</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="image">image5</property>
                        <property name="use_stock">False</property>
                        <property name="always_show_image">True</property>
                        <signal name="activate" handler="Config" swapped="no"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="ColorPickerMenu">
                        <property name="label">Color Picker</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="image">image4</property>
                        <property name="use_stock">False</property>
                        <signal name="activate" handler="ColorPicker" swapped="no"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="ZoomInMenu">
                        <property name="label">gtk-zoom-in</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <property name="always_show_image">True</property>
                        <signal name="activate" handler="ZoomIn" swapped="no"/>
                        <accelerator key="plus" signal="activate"/>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="ZoomOutMenu">
                        <property name="label">gtk-zoom-out</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                        <property name="always_show_image">True</property>
                        <signal name="activate" handler="ZoomOut" swapped="no"/>
                        <accelerator key="minus" signal="activate"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkProgressBar" id="progressbar">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="valign">end</property>
            <property name="hexpand">True</property>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkStatusbar" id="statusbar">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="valign">end</property>
            <property name="hexpand">True</property>
            <property name="orientation">vertical</property>
            <property name="spacing">2</property>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">4</property>
          </packing>
        </child>
        <child>
          <object class="GtkToolbar" id="toolbar">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="hexpand">True</property>
            <child>
              <object class="GtkToolButton" id="document_open">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">open image</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="document_save">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">export</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="document_save_as">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">export as</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="application_exit">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">exit</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolseparator1">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="drawmode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">set draw mode</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="drawmodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">set draw mode</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="colormode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">sec color mode</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="colormodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">set color mode</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolseparator2">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="openpath">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">mark current path open, start new</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="closedpath">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">mark current path closed, start new</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="blackmode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">mark next segment as black</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="blackmodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">mark next segment as black</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="whitemode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">mark next segment as white</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="whitemodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">mark next segment as white</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolseparator3">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="addmode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">add point</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="addmodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">add point</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="movemode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">move point</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="movemodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">move point</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="deletemode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">delete point</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="deletemodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">deletepoint</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolseparator4">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="selectmode">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">select path</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="selectmodesel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">select path</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparatorToolItem" id="toolseparator5">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="zoomin">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">zoom in</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkToolButton" id="zoomout">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">zoom out</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkBox" id="box1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="hexpand">True</property>
            <property name="vexpand">True</property>
            <child>
              <object class="GtkScrolledWindow" id="scrolledwindow">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="hexpand">True</property>
                <property name="vexpand">True</property>
                <property name="shadow_type">in</property>
                <child>
                  <object class="GtkViewport" id="viewport1">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="hexpand">True</property>
                    <property name="vexpand">True</property>
                    <child>
                      <object class="GtkDrawingArea" id="drawingarea">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="hexpand">True</property>
                        <property name="vexpand">True</property>
                        <signal name="button-press-event" handler="button_press_event" swapped="no"/>
                        <signal name="button-release-event" handler="button_release_event" swapped="no"/>
                        <signal name="draw" handler="cairo_draw" swapped="no"/>
                        <signal name="scroll-event" handler="mouse_scroll_event" swapped="no"/>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkAlignment" id="alignment1">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="vexpand">True</property>
                <property name="yalign">0</property>
                <child>
                  <object class="GtkBox" id="box2">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="vexpand">True</property>
                    <property name="orientation">vertical</property>
                    <child>
                      <object class="GtkScale" id="circleradiusscale">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="vexpand">True</property>
                        <property name="orientation">vertical</property>
                        <property name="adjustment">circleradiusadjustment</property>
                        <property name="round_digits">0</property>
                        <property name="digits">0</property>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">True</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkScale" id="sectoropeningscale">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="vexpand">True</property>
                        <property name="orientation">vertical</property>
                        <property name="adjustment">sectoropeningadjustment</property>
                        <property name="round_digits">0</property>
                        <property name="digits">0</property>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">True</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkScale" id="linewidthscale">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="vexpand">True</property>
                        <property name="orientation">vertical</property>
                        <property name="adjustment">linewidthadjustment</property>
                        <property name="round_digits">0</property>
                        <property name="digits">0</property>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">True</property>
                        <property name="position">2</property>
                      </packing>
                    </child>
                  </object>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">2</property>
          </packing>
        </child>
      </object>
    </child>
    <child type="titlebar">
      <placeholder/>
    </child>
  </object>
  <object class="GtkDialog" id="scribblesettingswindow">
    <property name="can_focus">False</property>
    <property name="title" translatable="yes">Scribble Settings</property>
    <property name="destroy_with_parent">True</property>
    <property name="type_hint">dialog</property>
    <property name="transient_for">window1</property>
    <signal name="delete-event" handler="hide_window" swapped="no"/>
    <signal name="destroy-event" handler="destroy" swapped="no"/>
    <child internal-child="vbox">
      <object class="GtkBox">
        <property name="can_focus">False</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox">
            <property name="can_focus">False</property>
            <property name="layout_style">end</property>
            <child>
              <object class="GtkButton" id="defaultvaluesbutton">
                <property name="label" translatable="yes">default values</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <signal name="clicked" handler="reset_slider_values" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="scribblesettingsok">
                <property name="label">gtk-close</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="can_default">True</property>
                <property name="has_default">True</property>
                <property name="receives_default">True</property>
                <property name="use_stock">True</property>
                <signal name="clicked" handler="hide_window" object="scribblesettingswindow" swapped="no"/>
                <style>
                  <class name="suggested-action"/>
                </style>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkBox">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="orientation">vertical</property>
            <child>
              <object class="GtkFrame">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label_xalign">0</property>
                <property name="shadow_type">none</property>
                <child>
                  <object class="GtkAlignment">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="left_padding">12</property>
                    <child>
                      <object class="GtkScale" id="circleradiusscale2">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="vexpand">True</property>
                        <property name="adjustment">circleradiusadjustment</property>
                        <property name="round_digits">0</property>
                        <property name="digits">0</property>
                      </object>
                    </child>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Sector/Circle radius:</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkFrame">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label_xalign">0</property>
                <property name="shadow_type">none</property>
                <child>
                  <object class="GtkAlignment">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="left_padding">12</property>
                    <child>
                      <object class="GtkScale" id="sectoropeningscale1">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="vexpand">True</property>
                        <property name="adjustment">sectoropeningadjustment</property>
                        <property name="round_digits">0</property>
                        <property name="digits">0</property>
                      </object>
                    </child>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Sector opening (in degrees):</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkFrame">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label_xalign">0</property>
                <property name="shadow_type">none</property>
                <child>
                  <object class="GtkAlignment">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="left_padding">12</property>
                    <child>
                      <object class="GtkScale" id="linewidthscale1">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="vexpand">True</property>
                        <property name="adjustment">linewidthadjustment</property>
                        <property name="round_digits">0</property>
                        <property name="digits">0</property>
                      </object>
                    </child>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Linewidth:</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">2</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
    <child>
      <placeholder/>
    </child>
  </object>
</interface>
'''


class scribbleicons:
    '''Our icons'''

    svgs={}         # will collect our icons as svg strings
    callbacks={}    # callback names associated to icons
    tooltips={}     # tooltips to display associated to icons
    UInames={}      # glade names associated to icons

    svgs['scribblemove']="""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface2">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 54.339844 C 33.742188 32.363281 49.921875 10.382812 57.328125 12.144531 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 12.144531 C 64.734375 13.902344 63.371094 39.394531 62.003906 64.890625 " transform="matrix(1,0,0,1,-5,1)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 65.890625 L 20.988281 55.339844 C 20.988281 59.996094 17.214844 63.769531 12.5625 63.769531 C 7.90625 63.769531 4.132812 59.996094 4.132812 55.339844 C 4.132812 50.6875 7.90625 46.910156 12.5625 46.910156 C 17.214844 46.910156 20.988281 50.6875 20.988281 55.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 13.144531 C 60.757812 17.796875 56.984375 21.570312 52.328125 21.570312 C 47.671875 21.570312 43.898438 17.796875 43.898438 13.144531 C 43.898438 8.488281 47.671875 4.714844 52.328125 4.714844 C 56.984375 4.714844 60.757812 8.488281 60.757812 13.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 65.890625 C 65.433594 70.546875 61.660156 74.320312 57.003906 74.320312 C 52.351562 74.320312 48.578125 70.546875 48.578125 65.890625 C 48.578125 61.234375 52.351562 57.460938 57.003906 57.460938 C 61.660156 57.460938 65.433594 61.234375 65.433594 65.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 55.339844 L 13.113281 63.75 C 9.019531 64.019531 5.328125 61.300781 4.367188 57.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 13.144531 L 44.800781 16.9375 C 42.953125 13.273438 44.011719 8.8125 47.308594 6.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 65.890625 L 51.929688 59.164062 C 55.203125 56.691406 59.78125 56.9375 62.773438 59.742188 "/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 54.339844 C 25.90625 57.582031 34.246094 60.824219 41.65625 62.582031 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 41.65625 62.582031 C 49.0625 64.339844 55.535156 64.617188 62.003906 64.890625 " transform="matrix(1,0,0,1,-5,1)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 65.890625 L 20.988281 55.339844 C 20.988281 59.996094 17.214844 63.769531 12.5625 63.769531 C 7.90625 63.769531 4.132812 59.996094 4.132812 55.339844 C 4.132812 50.6875 7.90625 46.910156 12.5625 46.910156 C 17.214844 46.910156 20.988281 50.6875 20.988281 55.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 45.082031 63.582031 C 45.082031 68.238281 41.308594 72.011719 36.65625 72.011719 C 32 72.011719 28.226562 68.238281 28.226562 63.582031 C 28.226562 58.925781 32 55.152344 36.65625 55.152344 C 41.308594 55.152344 45.082031 58.925781 45.082031 63.582031 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 65.890625 C 65.433594 70.546875 61.660156 74.320312 57.003906 74.320312 C 52.351562 74.320312 48.578125 70.546875 48.578125 65.890625 C 48.578125 61.234375 52.351562 57.460938 57.003906 57.460938 C 61.660156 57.460938 65.433594 61.234375 65.433594 65.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 55.339844 L 4.585938 58.066406 C 3.257812 54.183594 4.917969 49.910156 8.519531 47.945312 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 36.65625 63.582031 L 29.128906 67.375 C 27.28125 63.714844 28.339844 59.253906 31.636719 56.8125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 65.890625 L 50.335938 71.042969 C 47.828125 67.792969 48.023438 63.214844 50.796875 60.191406 "/>
<path style="fill:none;stroke-width:8.428571;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(20%,20%,20%);stroke-opacity:1;stroke-miterlimit:10;" d="M 54.191406 22.230469 L 44.789062 52.496094 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:8.428571;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(20%,20%,20%);stroke-opacity:1;stroke-miterlimit:10;" d="M 40.617188 44.5625 L 44.789062 52.496094 L 52.722656 48.324219 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
</g>
</svg>
    """
    callbacks['scribblemove']='move_toggle'
    tooltips['scribblemove']='set move mode'
    UInames['scribblemove']=['movemode']

    svgs['scribblemove_sel'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface27">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 54.339844 C 33.742188 32.363281 49.921875 10.382812 57.328125 12.144531 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 12.144531 C 64.734375 13.902344 63.371094 39.394531 62.003906 64.890625 " transform="matrix(1,0,0,1,-5,1)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 65.890625 L 20.988281 55.339844 C 20.988281 59.996094 17.214844 63.769531 12.5625 63.769531 C 7.90625 63.769531 4.132812 59.996094 4.132812 55.339844 C 4.132812 50.6875 7.90625 46.910156 12.5625 46.910156 C 17.214844 46.910156 20.988281 50.6875 20.988281 55.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 13.144531 C 60.757812 17.796875 56.984375 21.570312 52.328125 21.570312 C 47.671875 21.570312 43.898438 17.796875 43.898438 13.144531 C 43.898438 8.488281 47.671875 4.714844 52.328125 4.714844 C 56.984375 4.714844 60.757812 8.488281 60.757812 13.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 65.890625 C 65.433594 70.546875 61.660156 74.320312 57.003906 74.320312 C 52.351562 74.320312 48.578125 70.546875 48.578125 65.890625 C 48.578125 61.234375 52.351562 57.460938 57.003906 57.460938 C 61.660156 57.460938 65.433594 61.234375 65.433594 65.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 55.339844 L 13.113281 63.75 C 9.019531 64.019531 5.328125 61.300781 4.367188 57.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 13.144531 L 44.800781 16.9375 C 42.953125 13.273438 44.011719 8.8125 47.308594 6.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 65.890625 L 51.929688 59.164062 C 55.203125 56.691406 59.78125 56.9375 62.773438 59.742188 "/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 54.339844 C 25.90625 57.582031 34.246094 60.824219 41.65625 62.582031 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 41.65625 62.582031 C 49.0625 64.339844 55.535156 64.617188 62.003906 64.890625 " transform="matrix(1,0,0,1,-5,1)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 65.890625 L 20.988281 55.339844 C 20.988281 59.996094 17.214844 63.769531 12.5625 63.769531 C 7.90625 63.769531 4.132812 59.996094 4.132812 55.339844 C 4.132812 50.6875 7.90625 46.910156 12.5625 46.910156 C 17.214844 46.910156 20.988281 50.6875 20.988281 55.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 45.082031 63.582031 C 45.082031 68.238281 41.308594 72.011719 36.65625 72.011719 C 32 72.011719 28.226562 68.238281 28.226562 63.582031 C 28.226562 58.925781 32 55.152344 36.65625 55.152344 C 41.308594 55.152344 45.082031 58.925781 45.082031 63.582031 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 65.890625 C 65.433594 70.546875 61.660156 74.320312 57.003906 74.320312 C 52.351562 74.320312 48.578125 70.546875 48.578125 65.890625 C 48.578125 61.234375 52.351562 57.460938 57.003906 57.460938 C 61.660156 57.460938 65.433594 61.234375 65.433594 65.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 55.339844 L 4.585938 58.066406 C 3.257812 54.183594 4.917969 49.910156 8.519531 47.945312 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 36.65625 63.582031 L 29.128906 67.375 C 27.28125 63.714844 28.339844 59.253906 31.636719 56.8125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 65.890625 L 50.335938 71.042969 C 47.828125 67.792969 48.023438 63.214844 50.796875 60.191406 "/>
<path style="fill:none;stroke-width:8.428571;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(20%,20%,20%);stroke-opacity:1;stroke-miterlimit:10;" d="M 54.191406 22.230469 L 44.789062 52.496094 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:8.428571;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(20%,20%,20%);stroke-opacity:1;stroke-miterlimit:10;" d="M 40.617188 44.5625 L 44.789062 52.496094 L 52.722656 48.324219 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
</g>
</svg>
    """
    callbacks['scribblemove_sel']='move_toggle'
    tooltips['scribblemove_sel']='set move mode'
    UInames['scribblemove_sel']=['movemodesel']

    svgs['scribbledelete'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface7">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 134.339844 C 33.742188 112.363281 49.921875 90.382812 57.328125 92.144531 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 92.144531 C 64.734375 93.902344 63.371094 119.394531 62.003906 144.890625 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 66.890625 L 20.988281 56.339844 C 20.988281 60.996094 17.214844 64.769531 12.5625 64.769531 C 7.90625 64.769531 4.132812 60.996094 4.132812 56.339844 C 4.132812 51.6875 7.90625 47.910156 12.5625 47.910156 C 17.214844 47.910156 20.988281 51.6875 20.988281 56.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 14.144531 C 60.757812 18.796875 56.984375 22.570312 52.328125 22.570312 C 47.671875 22.570312 43.898438 18.796875 43.898438 14.144531 C 43.898438 9.488281 47.671875 5.714844 52.328125 5.714844 C 56.984375 5.714844 60.757812 9.488281 60.757812 14.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 66.890625 C 65.433594 71.546875 61.660156 75.320312 57.003906 75.320312 C 52.351562 75.320312 48.578125 71.546875 48.578125 66.890625 C 48.578125 62.234375 52.351562 58.460938 57.003906 58.460938 C 61.660156 58.460938 65.433594 62.234375 65.433594 66.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 56.339844 L 13.113281 64.75 C 9.019531 65.019531 5.328125 62.300781 4.367188 58.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 14.144531 L 44.800781 17.9375 C 42.953125 14.273438 44.011719 9.8125 47.308594 7.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 66.890625 L 51.929688 60.164062 C 55.203125 57.691406 59.78125 57.9375 62.773438 60.742188 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 35.199219 17 C 35.199219 26.777344 27.277344 34.699219 17.5 34.699219 C 7.722656 34.699219 -0.199219 26.777344 -0.199219 17 C -0.199219 7.222656 7.722656 -0.699219 17.5 -0.699219 C 27.277344 -0.699219 35.199219 7.222656 35.199219 17 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(60%,60%,60%);fill-opacity:1;" d="M 32.390625 17 C 32.390625 25.222656 25.722656 31.890625 17.5 31.890625 C 9.277344 31.890625 2.609375 25.222656 2.609375 17 C 2.609375 8.777344 9.277344 2.109375 17.5 2.109375 C 25.722656 2.109375 32.390625 8.777344 32.390625 17 "/>
<path style="fill:none;stroke-width:7.304762;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(84.705882%,11.764706%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 15 95 L 30 95 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
</g>
</svg>
    """
    callbacks['scribbledelete']='delete_toggle'
    tooltips['scribbledelete']= 'set delete mode'
    UInames['scribbledelete']=['deletemode']

    svgs['scribbledelete_sel'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface32">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 134.339844 C 33.742188 112.363281 49.921875 90.382812 57.328125 92.144531 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 92.144531 C 64.734375 93.902344 63.371094 119.394531 62.003906 144.890625 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 66.890625 L 20.988281 56.339844 C 20.988281 60.996094 17.214844 64.769531 12.5625 64.769531 C 7.90625 64.769531 4.132812 60.996094 4.132812 56.339844 C 4.132812 51.6875 7.90625 47.910156 12.5625 47.910156 C 17.214844 47.910156 20.988281 51.6875 20.988281 56.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 14.144531 C 60.757812 18.796875 56.984375 22.570312 52.328125 22.570312 C 47.671875 22.570312 43.898438 18.796875 43.898438 14.144531 C 43.898438 9.488281 47.671875 5.714844 52.328125 5.714844 C 56.984375 5.714844 60.757812 9.488281 60.757812 14.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 66.890625 C 65.433594 71.546875 61.660156 75.320312 57.003906 75.320312 C 52.351562 75.320312 48.578125 71.546875 48.578125 66.890625 C 48.578125 62.234375 52.351562 58.460938 57.003906 58.460938 C 61.660156 58.460938 65.433594 62.234375 65.433594 66.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 56.339844 L 13.113281 64.75 C 9.019531 65.019531 5.328125 62.300781 4.367188 58.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 14.144531 L 44.800781 17.9375 C 42.953125 14.273438 44.011719 9.8125 47.308594 7.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 66.890625 L 51.929688 60.164062 C 55.203125 57.691406 59.78125 57.9375 62.773438 60.742188 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 35.199219 17 C 35.199219 26.777344 27.277344 34.699219 17.5 34.699219 C 7.722656 34.699219 -0.199219 26.777344 -0.199219 17 C -0.199219 7.222656 7.722656 -0.699219 17.5 -0.699219 C 27.277344 -0.699219 35.199219 7.222656 35.199219 17 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(60%,60%,60%);fill-opacity:1;" d="M 32.390625 17 C 32.390625 25.222656 25.722656 31.890625 17.5 31.890625 C 9.277344 31.890625 2.609375 25.222656 2.609375 17 C 2.609375 8.777344 9.277344 2.109375 17.5 2.109375 C 25.722656 2.109375 32.390625 8.777344 32.390625 17 "/>
<path style="fill:none;stroke-width:7.304762;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(84.705882%,11.764706%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 15 95 L 30 95 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
</g>
</svg>
    """
    callbacks['scribbledelete_sel']= 'delete_toggle'
    tooltips['scribbledelete_sel']= 'set delete mode'
    UInames['scribbledelete_sel']=['deletemodesel']


    svgs['scribbleadd'] ="""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface12">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 214.339844 C 33.742188 192.363281 49.921875 170.382812 57.328125 172.144531 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 172.144531 C 64.734375 173.902344 63.371094 199.394531 62.003906 224.890625 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 66.890625 L 20.988281 56.339844 C 20.988281 60.996094 17.214844 64.769531 12.5625 64.769531 C 7.90625 64.769531 4.132812 60.996094 4.132812 56.339844 C 4.132812 51.6875 7.90625 47.910156 12.5625 47.910156 C 17.214844 47.910156 20.988281 51.6875 20.988281 56.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 14.144531 C 60.757812 18.796875 56.984375 22.570312 52.328125 22.570312 C 47.671875 22.570312 43.898438 18.796875 43.898438 14.144531 C 43.898438 9.488281 47.671875 5.714844 52.328125 5.714844 C 56.984375 5.714844 60.757812 9.488281 60.757812 14.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 66.890625 C 65.433594 71.546875 61.660156 75.320312 57.003906 75.320312 C 52.351562 75.320312 48.578125 71.546875 48.578125 66.890625 C 48.578125 62.234375 52.351562 58.460938 57.003906 58.460938 C 61.660156 58.460938 65.433594 62.234375 65.433594 66.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 56.339844 L 13.113281 64.75 C 9.019531 65.019531 5.328125 62.300781 4.367188 58.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 14.144531 L 44.800781 17.9375 C 42.953125 14.273438 44.011719 9.8125 47.308594 7.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 66.890625 L 51.929688 60.164062 C 55.203125 57.691406 59.78125 57.9375 62.773438 60.742188 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 35.199219 17 C 35.199219 26.777344 27.277344 34.699219 17.5 34.699219 C 7.722656 34.699219 -0.199219 26.777344 -0.199219 17 C -0.199219 7.222656 7.722656 -0.699219 17.5 -0.699219 C 27.277344 -0.699219 35.199219 7.222656 35.199219 17 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(60%,60%,60%);fill-opacity:1;" d="M 32.390625 17 C 32.390625 25.222656 25.722656 31.890625 17.5 31.890625 C 9.277344 31.890625 2.609375 25.222656 2.609375 17 C 2.609375 8.777344 9.277344 2.109375 17.5 2.109375 C 25.722656 2.109375 32.390625 8.777344 32.390625 17 "/>
<path style="fill:none;stroke-width:7.304762;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 15 175 L 30 175 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:7.304762;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 22.5 182.5 L 22.5 167.5 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
</g>
</svg>
    """
    callbacks['scribbleadd']='add_toggle'
    tooltips['scribbleadd']= 'set add mode'
    UInames['scribbleadd']=['addmode']

    svgs['scribbleadd_sel']="""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface37">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 214.339844 C 33.742188 192.363281 49.921875 170.382812 57.328125 172.144531 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 172.144531 C 64.734375 173.902344 63.371094 199.394531 62.003906 224.890625 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 66.890625 L 20.988281 56.339844 C 20.988281 60.996094 17.214844 64.769531 12.5625 64.769531 C 7.90625 64.769531 4.132812 60.996094 4.132812 56.339844 C 4.132812 51.6875 7.90625 47.910156 12.5625 47.910156 C 17.214844 47.910156 20.988281 51.6875 20.988281 56.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 14.144531 C 60.757812 18.796875 56.984375 22.570312 52.328125 22.570312 C 47.671875 22.570312 43.898438 18.796875 43.898438 14.144531 C 43.898438 9.488281 47.671875 5.714844 52.328125 5.714844 C 56.984375 5.714844 60.757812 9.488281 60.757812 14.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 66.890625 C 65.433594 71.546875 61.660156 75.320312 57.003906 75.320312 C 52.351562 75.320312 48.578125 71.546875 48.578125 66.890625 C 48.578125 62.234375 52.351562 58.460938 57.003906 58.460938 C 61.660156 58.460938 65.433594 62.234375 65.433594 66.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 56.339844 L 13.113281 64.75 C 9.019531 65.019531 5.328125 62.300781 4.367188 58.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 14.144531 L 44.800781 17.9375 C 42.953125 14.273438 44.011719 9.8125 47.308594 7.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 66.890625 L 51.929688 60.164062 C 55.203125 57.691406 59.78125 57.9375 62.773438 60.742188 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 35.199219 17 C 35.199219 26.777344 27.277344 34.699219 17.5 34.699219 C 7.722656 34.699219 -0.199219 26.777344 -0.199219 17 C -0.199219 7.222656 7.722656 -0.699219 17.5 -0.699219 C 27.277344 -0.699219 35.199219 7.222656 35.199219 17 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(60%,60%,60%);fill-opacity:1;" d="M 32.390625 17 C 32.390625 25.222656 25.722656 31.890625 17.5 31.890625 C 9.277344 31.890625 2.609375 25.222656 2.609375 17 C 2.609375 8.777344 9.277344 2.109375 17.5 2.109375 C 25.722656 2.109375 32.390625 8.777344 32.390625 17 "/>
<path style="fill:none;stroke-width:7.304762;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 15 175 L 30 175 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:7.304762;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 22.5 182.5 L 22.5 167.5 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
</g>
</svg>
    """
    callbacks['scribbleadd_sel']='add_toggle'
    tooltips['scribbleadd_sel']='set add mode'
    UInames['scribbleadd_sel']=['addmodesel']

    svgs['scribbleopen'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="77pt" height="77pt" viewBox="0 0 77 77" version="1.1">
<g id="surface17">
<rect x="0" y="0" width="77" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 294.339844 C 33.742188 272.363281 49.921875 250.382812 57.328125 252.144531 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 252.144531 C 64.734375 253.902344 63.371094 279.394531 62.003906 304.890625 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 57.003906 65.890625 L 20.988281 55.339844 C 20.988281 59.996094 17.214844 63.769531 12.5625 63.769531 C 7.90625 63.769531 4.132812 59.996094 4.132812 55.339844 C 4.132812 50.6875 7.90625 46.910156 12.5625 46.910156 C 17.214844 46.910156 20.988281 50.6875 20.988281 55.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 13.144531 C 60.757812 17.796875 56.984375 21.570312 52.328125 21.570312 C 47.671875 21.570312 43.898438 17.796875 43.898438 13.144531 C 43.898438 8.488281 47.671875 4.714844 52.328125 4.714844 C 56.984375 4.714844 60.757812 8.488281 60.757812 13.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 65.890625 C 65.433594 70.546875 61.660156 74.320312 57.003906 74.320312 C 52.351562 74.320312 48.578125 70.546875 48.578125 65.890625 C 48.578125 61.234375 52.351562 57.460938 57.003906 57.460938 C 61.660156 57.460938 65.433594 61.234375 65.433594 65.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 55.339844 L 13.113281 63.75 C 9.019531 64.019531 5.328125 61.300781 4.367188 57.3125 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 13.144531 L 44.800781 16.9375 C 42.953125 13.273438 44.011719 8.8125 47.308594 6.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 65.890625 L 51.929688 59.164062 C 55.203125 56.691406 59.78125 56.9375 62.773438 59.742188 "/>
<path style="fill:none;stroke-width:10.114286;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(100%,100%,100%);stroke-opacity:1;stroke-miterlimit:10;" d="M 33.738281 255 C 33.738281 261.207031 28.707031 266.238281 22.5 266.238281 C 16.292969 266.238281 11.261719 261.207031 11.261719 255 C 11.261719 248.792969 16.292969 243.761719 22.5 243.761719 C 28.707031 243.761719 33.738281 248.792969 33.738281 255 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(30%,30%,30%);stroke-opacity:1;stroke-miterlimit:10;" d="M 33.738281 255 C 33.738281 261.207031 28.707031 266.238281 22.5 266.238281 C 16.292969 266.238281 11.261719 261.207031 11.261719 255 C 11.261719 248.792969 16.292969 243.761719 22.5 243.761719 C 28.707031 243.761719 33.738281 248.792969 33.738281 255 " transform="matrix(1,0,0,1,-5,-239)"/>
</g>
</svg>
    """
    callbacks['scribbleopen'] ='open_toggle'
    tooltips['scribbleopen']='mark current path as open, start new path'
    UInames['scribbleopen']=['openpath']


    svgs['scribbleclosed'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="77pt" height="77pt" viewBox="0 0 77 77" version="1.1">
<g id="surface22">
<rect x="0" y="0" width="77" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 17.5625 374.339844 C 16 356.757812 42.511719 328.625 57.328125 332.144531 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 57.328125 332.144531 C 72.140625 335.660156 75.261719 370.824219 62.003906 384.890625 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 62.003906 384.890625 C 48.75 398.957031 19.121094 391.921875 17.5625 374.339844 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 12.5625 51.339844 L 20.988281 51.339844 C 20.988281 55.996094 17.214844 59.769531 12.5625 59.769531 C 7.90625 59.769531 4.132812 55.996094 4.132812 51.339844 C 4.132812 46.6875 7.90625 42.910156 12.5625 42.910156 C 17.214844 42.910156 20.988281 46.6875 20.988281 51.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 60.757812 9.144531 C 60.757812 13.796875 56.984375 17.570312 52.328125 17.570312 C 47.671875 17.570312 43.898438 13.796875 43.898438 9.144531 C 43.898438 4.488281 47.671875 0.714844 52.328125 0.714844 C 56.984375 0.714844 60.757812 4.488281 60.757812 9.144531 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 65.433594 61.890625 C 65.433594 66.546875 61.660156 70.320312 57.003906 70.320312 C 52.351562 70.320312 48.578125 66.546875 48.578125 61.890625 C 48.578125 57.234375 52.351562 53.460938 57.003906 53.460938 C 61.660156 53.460938 65.433594 57.234375 65.433594 61.890625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,0%,0%);fill-opacity:1;" d="M 20.988281 51.339844 C 20.988281 55.996094 17.214844 59.769531 12.5625 59.769531 C 7.90625 59.769531 4.132812 55.996094 4.132812 51.339844 C 4.132812 46.6875 7.90625 42.910156 12.5625 42.910156 C 17.214844 42.910156 20.988281 46.6875 20.988281 51.339844 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 51.339844 L 18.539062 57.28125 C 15.648438 60.191406 11.082031 60.597656 7.722656 58.242188 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 52.328125 9.144531 L 44.800781 12.9375 C 42.953125 9.273438 44.011719 4.8125 47.308594 2.371094 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 57.003906 61.890625 L 57.476562 53.476562 C 61.570312 53.703125 64.90625 56.847656 65.378906 60.921875 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(100%,100%,100%);fill-opacity:1;" d="M 12.5625 51.339844 L 18.539062 57.28125 C 15.648438 60.191406 11.082031 60.597656 7.722656 58.242188 "/>
<path style="fill:none;stroke-width:10.114286;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(100%,100%,100%);stroke-opacity:1;stroke-miterlimit:10;" d="M 28.117188 348.734375 C 24.640625 350.738281 20.359375 350.738281 16.882812 348.734375 C 13.402344 346.726562 11.261719 343.015625 11.261719 339 C 11.261719 334.984375 13.402344 331.273438 16.882812 329.265625 C 20.359375 327.261719 24.640625 327.261719 28.117188 329.265625 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(30%,30%,30%);stroke-opacity:1;stroke-miterlimit:10;" d="M 28.117188 348.734375 C 24.640625 350.738281 20.359375 350.738281 16.882812 348.734375 C 13.402344 346.726562 11.261719 343.015625 11.261719 339 C 11.261719 334.984375 13.402344 331.273438 16.882812 329.265625 C 20.359375 327.261719 24.640625 327.261719 28.117188 329.265625 " transform="matrix(1,0,0,1,-5,-323)"/>
</g>
</svg>
    """
    callbacks['scribbleclosed']='closed_toggle'
    tooltips['scribbleclosed']='mark current path as closed, start new path'
    UInames['scribbleclosed']=['closedpath']


    svgs['scribblewhite']="""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface52">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 12 L 68 12 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 12 L 68 63 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 63 L 11 63 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 63 L 11 12 " transform="matrix(1,0,0,1,-5,1)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(99%,99%,99%);fill-opacity:1;" d="M 6 13 L 63 13 L 63 64 L 6 64 L 6 13 "/>
</g>
</svg>
    """
    callbacks['scribblewhite'] ='white_toggle'
    tooltips['scribblewhite']='mark next segment as white'
    UInames['scribblewhite']=['whitemode']

    svgs['scribblewhite_sel']="""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface77">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 65 L 87 10 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 12 L 68 12 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 12 L 68 63 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 63 L 11 63 " transform="matrix(1,0,0,1,-5,1)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 63 L 11 12 " transform="matrix(1,0,0,1,-5,1)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(99%,99%,99%);fill-opacity:1;" d="M 6 13 L 63 13 L 63 64 L 6 64 L 6 13 "/>
</g>
</svg>
    """
    callbacks['scribblewhite_sel']='white_toggle'
    tooltips['scribblewhite_sel']='mark next segment as white'
    UInames['scribblewhite_sel']=['whitemodesel']

    svgs['scribbleblack'] ="""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface57">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 91 L 68 91 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 91 L 68 142 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 142 L 11 142 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 142 L 11 91 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 6 13 L 63 13 L 63 64 L 6 64 L 6 13 "/>
</g>
</svg>
    """
    callbacks['scribbleblack']='black_toggle'
    tooltips['scribbleblack']='mark next segment as black'
    UInames['scribbleblack']=['blackmode']

    svgs['scribbleblack_sel'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface82">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 144 L 87 89 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 91 L 68 91 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 91 L 68 142 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 142 L 11 142 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 142 L 11 91 " transform="matrix(1,0,0,1,-5,-78)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 6 13 L 63 13 L 63 64 L 6 64 L 6 13 "/>
</g>
</svg>
    """
    callbacks['scribbleblack_sel']='black_toggle'
    tooltips['scribbleblack_sel']='mark next segment as black'
    UInames['scribbleblack_sel']=['blackmodesel']

    svgs['scribbleselect_path'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface62">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 35 228 C 37.734375 227.804688 43.8125 227.089844 47.601562 226.199219 C 51.386719 225.3125 52.875 224.246094 54.601562 222.398438 C 56.324219 220.550781 58.28125 217.917969 59.300781 216.199219 C 60.320312 214.480469 60.398438 213.671875 60.5 212 C 60.601562 210.328125 60.726562 207.789062 59.699219 205.300781 C 58.671875 202.8125 56.496094 200.375 55 198.601562 C 53.503906 196.828125 52.691406 195.714844 48.300781 194.199219 C 43.90625 192.683594 35.933594 190.761719 32.300781 189.199219 C 28.664062 187.640625 29.367188 186.441406 29.601562 184.800781 C 29.832031 183.160156 29.601562 181.074219 30.800781 179 C 32 176.925781 34.636719 174.863281 36.601562 173.300781 C 38.566406 171.738281 39.859375 170.675781 42.5 170.601562 C 45.140625 170.527344 49.125 171.4375 51.398438 171.898438 C 53.671875 172.359375 54.234375 172.367188 54.601562 173.601562 C 54.96875 174.832031 55.140625 177.289062 56 178.398438 C 56.859375 179.511719 58.398438 179.28125 59.5 178.800781 C 60.601562 178.320312 61.257812 177.589844 61.300781 175.898438 C 61.339844 174.210938 60.765625 171.5625 59.300781 169.699219 C 57.835938 167.835938 55.484375 166.757812 52.5 165.898438 C 49.515625 165.042969 45.890625 164.40625 43 164.398438 C 40.109375 164.394531 37.945312 165.023438 35.300781 166.699219 C 32.652344 168.375 29.523438 171.101562 27.398438 173.5 C 25.277344 175.898438 24.160156 177.972656 23.800781 180.601562 C 23.4375 183.226562 23.832031 186.410156 24.601562 188.800781 C 25.367188 191.191406 26.511719 192.792969 28.699219 194.199219 C 30.886719 195.605469 34.121094 196.8125 37.5 197.601562 C 40.878906 198.386719 44.402344 198.75 47.300781 200.300781 C 50.199219 201.851562 52.472656 204.589844 53.699219 206.601562 C 54.929688 208.609375 55.113281 209.886719 54.5 211.601562 C 53.886719 213.3125 52.476562 215.457031 51.101562 217.101562 C 49.722656 218.742188 48.378906 219.886719 45.5 220.601562 C 42.621094 221.316406 38.207031 221.601562 35.101562 221.601562 C 31.992188 221.597656 30.191406 221.308594 28.300781 219.101562 C 26.410156 216.890625 24.429688 212.761719 22.898438 211.398438 C 21.371094 210.039062 20.289062 211.445312 19.5 212.199219 C 18.710938 212.957031 18.210938 213.0625 18.800781 215 C 19.390625 216.9375 21.070312 220.703125 23.699219 223.101562 C 26.332031 225.496094 29.917969 226.523438 31.398438 227.199219 C 32.882812 227.875 32.265625 228.195312 35 228 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;stroke-width:6.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 35 228 C 37.734375 227.804688 43.8125 227.089844 47.601562 226.199219 C 51.386719 225.3125 52.875 224.246094 54.601562 222.398438 C 56.324219 220.550781 58.28125 217.917969 59.300781 216.199219 C 60.320312 214.480469 60.398438 213.671875 60.5 212 C 60.601562 210.328125 60.726562 207.789062 59.699219 205.300781 C 58.671875 202.8125 56.496094 200.375 55 198.601562 C 53.503906 196.828125 52.691406 195.714844 48.300781 194.199219 C 43.90625 192.683594 35.933594 190.761719 32.300781 189.199219 C 28.664062 187.640625 29.367188 186.441406 29.601562 184.800781 C 29.832031 183.160156 29.601562 181.074219 30.800781 179 C 32 176.925781 34.636719 174.863281 36.601562 173.300781 C 38.566406 171.738281 39.859375 170.675781 42.5 170.601562 C 45.140625 170.527344 49.125 171.4375 51.398438 171.898438 C 53.671875 172.359375 54.234375 172.367188 54.601562 173.601562 C 54.96875 174.832031 55.140625 177.289062 56 178.398438 C 56.859375 179.511719 58.398438 179.28125 59.5 178.800781 C 60.601562 178.320312 61.257812 177.589844 61.300781 175.898438 C 61.339844 174.210938 60.765625 171.5625 59.300781 169.699219 C 57.835938 167.835938 55.484375 166.757812 52.5 165.898438 C 49.515625 165.042969 45.890625 164.40625 43 164.398438 C 40.109375 164.394531 37.945312 165.023438 35.300781 166.699219 C 32.652344 168.375 29.523438 171.101562 27.398438 173.5 C 25.277344 175.898438 24.160156 177.972656 23.800781 180.601562 C 23.4375 183.226562 23.832031 186.410156 24.601562 188.800781 C 25.367188 191.191406 26.511719 192.792969 28.699219 194.199219 C 30.886719 195.605469 34.121094 196.8125 37.5 197.601562 C 40.878906 198.386719 44.402344 198.75 47.300781 200.300781 C 50.199219 201.851562 52.472656 204.589844 53.699219 206.601562 C 54.929688 208.609375 55.113281 209.886719 54.5 211.601562 C 53.886719 213.3125 52.476562 215.457031 51.101562 217.101562 C 49.722656 218.742188 48.378906 219.886719 45.5 220.601562 C 42.621094 221.316406 38.207031 221.601562 35.101562 221.601562 C 31.992188 221.597656 30.191406 221.308594 28.300781 219.101562 C 26.410156 216.890625 24.429688 212.761719 22.898438 211.398438 C 21.371094 210.039062 20.289062 211.445312 19.5 212.199219 C 18.710938 212.957031 18.210938 213.0625 18.800781 215 C 19.390625 216.9375 21.070312 220.703125 23.699219 223.101562 C 26.332031 225.496094 29.917969 226.523438 31.398438 227.199219 C 32.882812 227.875 32.265625 228.195312 35 228 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 50 183 L 25 213 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 24 202 L 25 213 L 36 212 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 50 183 L 25 213 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 24 202 L 25 213 L 36 212 " transform="matrix(1,0,0,1,-5,-158)"/>
</g>
</svg>
    """
    callbacks['scribbleselect_path']='select_mode_toggle'
    tooltips['scribbleselect_path']='select path mode'
    UInames['scribbleselect_path']=['selectmode']

    svgs['scribbleselect_path_sel'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface87">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 224 L 87 169 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 35 228 C 37.734375 227.804688 43.8125 227.089844 47.601562 226.199219 C 51.386719 225.3125 52.875 224.246094 54.601562 222.398438 C 56.324219 220.550781 58.28125 217.917969 59.300781 216.199219 C 60.320312 214.480469 60.398438 213.671875 60.5 212 C 60.601562 210.328125 60.726562 207.789062 59.699219 205.300781 C 58.671875 202.8125 56.496094 200.375 55 198.601562 C 53.503906 196.828125 52.691406 195.714844 48.300781 194.199219 C 43.90625 192.683594 35.933594 190.761719 32.300781 189.199219 C 28.664062 187.640625 29.367188 186.441406 29.601562 184.800781 C 29.832031 183.160156 29.601562 181.074219 30.800781 179 C 32 176.925781 34.636719 174.863281 36.601562 173.300781 C 38.566406 171.738281 39.859375 170.675781 42.5 170.601562 C 45.140625 170.527344 49.125 171.4375 51.398438 171.898438 C 53.671875 172.359375 54.234375 172.367188 54.601562 173.601562 C 54.96875 174.832031 55.140625 177.289062 56 178.398438 C 56.859375 179.511719 58.398438 179.28125 59.5 178.800781 C 60.601562 178.320312 61.257812 177.589844 61.300781 175.898438 C 61.339844 174.210938 60.765625 171.5625 59.300781 169.699219 C 57.835938 167.835938 55.484375 166.757812 52.5 165.898438 C 49.515625 165.042969 45.890625 164.40625 43 164.398438 C 40.109375 164.394531 37.945312 165.023438 35.300781 166.699219 C 32.652344 168.375 29.523438 171.101562 27.398438 173.5 C 25.277344 175.898438 24.160156 177.972656 23.800781 180.601562 C 23.4375 183.226562 23.832031 186.410156 24.601562 188.800781 C 25.367188 191.191406 26.511719 192.792969 28.699219 194.199219 C 30.886719 195.605469 34.121094 196.8125 37.5 197.601562 C 40.878906 198.386719 44.402344 198.75 47.300781 200.300781 C 50.199219 201.851562 52.472656 204.589844 53.699219 206.601562 C 54.929688 208.609375 55.113281 209.886719 54.5 211.601562 C 53.886719 213.3125 52.476562 215.457031 51.101562 217.101562 C 49.722656 218.742188 48.378906 219.886719 45.5 220.601562 C 42.621094 221.316406 38.207031 221.601562 35.101562 221.601562 C 31.992188 221.597656 30.191406 221.308594 28.300781 219.101562 C 26.410156 216.890625 24.429688 212.761719 22.898438 211.398438 C 21.371094 210.039062 20.289062 211.445312 19.5 212.199219 C 18.710938 212.957031 18.210938 213.0625 18.800781 215 C 19.390625 216.9375 21.070312 220.703125 23.699219 223.101562 C 26.332031 225.496094 29.917969 226.523438 31.398438 227.199219 C 32.882812 227.875 32.265625 228.195312 35 228 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;stroke-width:6.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 35 228 C 37.734375 227.804688 43.8125 227.089844 47.601562 226.199219 C 51.386719 225.3125 52.875 224.246094 54.601562 222.398438 C 56.324219 220.550781 58.28125 217.917969 59.300781 216.199219 C 60.320312 214.480469 60.398438 213.671875 60.5 212 C 60.601562 210.328125 60.726562 207.789062 59.699219 205.300781 C 58.671875 202.8125 56.496094 200.375 55 198.601562 C 53.503906 196.828125 52.691406 195.714844 48.300781 194.199219 C 43.90625 192.683594 35.933594 190.761719 32.300781 189.199219 C 28.664062 187.640625 29.367188 186.441406 29.601562 184.800781 C 29.832031 183.160156 29.601562 181.074219 30.800781 179 C 32 176.925781 34.636719 174.863281 36.601562 173.300781 C 38.566406 171.738281 39.859375 170.675781 42.5 170.601562 C 45.140625 170.527344 49.125 171.4375 51.398438 171.898438 C 53.671875 172.359375 54.234375 172.367188 54.601562 173.601562 C 54.96875 174.832031 55.140625 177.289062 56 178.398438 C 56.859375 179.511719 58.398438 179.28125 59.5 178.800781 C 60.601562 178.320312 61.257812 177.589844 61.300781 175.898438 C 61.339844 174.210938 60.765625 171.5625 59.300781 169.699219 C 57.835938 167.835938 55.484375 166.757812 52.5 165.898438 C 49.515625 165.042969 45.890625 164.40625 43 164.398438 C 40.109375 164.394531 37.945312 165.023438 35.300781 166.699219 C 32.652344 168.375 29.523438 171.101562 27.398438 173.5 C 25.277344 175.898438 24.160156 177.972656 23.800781 180.601562 C 23.4375 183.226562 23.832031 186.410156 24.601562 188.800781 C 25.367188 191.191406 26.511719 192.792969 28.699219 194.199219 C 30.886719 195.605469 34.121094 196.8125 37.5 197.601562 C 40.878906 198.386719 44.402344 198.75 47.300781 200.300781 C 50.199219 201.851562 52.472656 204.589844 53.699219 206.601562 C 54.929688 208.609375 55.113281 209.886719 54.5 211.601562 C 53.886719 213.3125 52.476562 215.457031 51.101562 217.101562 C 49.722656 218.742188 48.378906 219.886719 45.5 220.601562 C 42.621094 221.316406 38.207031 221.601562 35.101562 221.601562 C 31.992188 221.597656 30.191406 221.308594 28.300781 219.101562 C 26.410156 216.890625 24.429688 212.761719 22.898438 211.398438 C 21.371094 210.039062 20.289062 211.445312 19.5 212.199219 C 18.710938 212.957031 18.210938 213.0625 18.800781 215 C 19.390625 216.9375 21.070312 220.703125 23.699219 223.101562 C 26.332031 225.496094 29.917969 226.523438 31.398438 227.199219 C 32.882812 227.875 32.265625 228.195312 35 228 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 50 183 L 25 213 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 24 202 L 25 213 L 36 212 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 50 183 L 25 213 " transform="matrix(1,0,0,1,-5,-158)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 24 202 L 25 213 L 36 212 " transform="matrix(1,0,0,1,-5,-158)"/>
</g>
</svg>
    """
    callbacks['scribbleselect_path_sel']='select_mode_toggle'
    tooltips['scribbleselect_path_sel']='select path mode'
    UInames['scribbleselect_path_sel']=['selectmodesel']


    svgs['scribbledraw'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface67">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 305 L 87 250 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 305 L 87 250 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(40%,40%,40%);fill-opacity:1;" d="M 6 69 L 9.941406 55.566406 C 14.515625 56.910156 18.089844 60.484375 19.433594 65.058594 "/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(40%,40%,40%);stroke-opacity:1;stroke-miterlimit:10;" d="M 56.628906 248.808594 L 16.628906 288.808594 L 11 308 L 30.191406 302.371094 L 70.191406 262.371094 L 56.628906 248.808594 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style="fill:none;stroke-width:2.809524;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(40%,40%,40%);stroke-opacity:1;stroke-miterlimit:10;" d="M 63.410156 255.589844 L 26.554688 292.445312 " transform="matrix(1,0,0,1,-5,-239)"/>
</g>
</svg>
    """
    callbacks['scribbledraw']='draw_mode_toggle'
    tooltips['scribbledraw']='select draw mode'
    UInames['scribbledraw']=['drawmode']

    svgs['scribbledraw_sel'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface92">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 305 L 87 250 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 305 L 87 250 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(40%,40%,40%);fill-opacity:1;" d="M 6 69 L 9.941406 55.566406 C 14.515625 56.910156 18.089844 60.484375 19.433594 65.058594 "/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(40%,40%,40%);stroke-opacity:1;stroke-miterlimit:10;" d="M 56.628906 248.808594 L 16.628906 288.808594 L 11 308 L 30.191406 302.371094 L 70.191406 262.371094 L 56.628906 248.808594 " transform="matrix(1,0,0,1,-5,-239)"/>
<path style="fill:none;stroke-width:2.809524;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(40%,40%,40%);stroke-opacity:1;stroke-miterlimit:10;" d="M 63.410156 255.589844 L 26.554688 292.445312 " transform="matrix(1,0,0,1,-5,-239)"/>
</g>
</svg>
    """
    callbacks['scribbledraw_sel']='draw_mode_toggle'
    tooltips['scribbledraw_sel']= 'select draw mode'
    UInames['scribbledraw_sel']=['drawmodesel']

    svgs['scribblecolor'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface72">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 389 L 87 334 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(80%,80%,80%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 389 L 87 334 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 336 L 68 336 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 336 L 68 387 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 387 L 11 387 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 387 L 11 336 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 6 13 L 63 13 L 6 64 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(99%,99%,99%);fill-opacity:1;" d="M 63 13 L 6 64 L 63 64 "/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 39.5 361.5 L 29.5 351.5 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 37.5 355.5 L 29.5 351.5 L 33.5 359.5 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 39.5 361.5 L 49.5 371.5 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 41.5 367.5 L 49.5 371.5 L 45.5 363.5 " transform="matrix(1,0,0,1,-5,-323)"/>
</g>
</svg>
    """
    callbacks['scribblecolor']='color_mode_toggle'
    tooltips['scribblecolor']= 'select color mode'
    UInames['scribblecolor']=['colormode']


    svgs['scribblecolor_sel'] = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="93pt" height="77pt" viewBox="0 0 93 77" version="1.1">
<g id="surface97">
<rect x="0" y="0" width="93" height="77" style="fill:rgb(100%,100%,100%);fill-opacity:1;stroke:none;"/>
<path style="fill:none;stroke-width:21.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 389 L 87 334 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:14.47619;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(19.607843%,71.372549%,21.960784%);stroke-opacity:1;stroke-miterlimit:10;" d="M 87 389 L 87 334 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 336 L 68 336 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 336 L 68 387 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 68 387 L 11 387 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:11.238095;stroke-linecap:round;stroke-linejoin:miter;stroke:rgb(50%,50%,50%);stroke-opacity:1;stroke-miterlimit:10;" d="M 11 387 L 11 336 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 6 13 L 63 13 L 6 64 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(99%,99%,99%);fill-opacity:1;" d="M 63 13 L 6 64 L 63 64 "/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 39.5 361.5 L 29.5 351.5 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(99%,99%,99%);stroke-opacity:1;stroke-miterlimit:10;" d="M 37.5 355.5 L 29.5 351.5 L 33.5 359.5 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 39.5 361.5 L 49.5 371.5 " transform="matrix(1,0,0,1,-5,-323)"/>
<path style="fill:none;stroke-width:5.619048;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 41.5 367.5 L 49.5 371.5 L 45.5 363.5 " transform="matrix(1,0,0,1,-5,-323)"/>
</g>
</svg>
    """
    callbacks['scribblecolor_sel']='color_mode_toggle'
    tooltips['scribblecolor_sel']= 'select color mode'
    UInames['scribblecolor_sel']=['colormodesel']


    svgs['zoom_in'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
       d="M 4 4 L 4 9 L 5 9 L 5 5 L 9 5 L 9 4 L 4 4 z M 11 4 L 11 5 L 15 5 L 15 4 L 11 4 z M 17 4 L 17 5 L 21 5 L 21 4 L 17 4 z M 23 4 L 23 5 L 27 5 L 27 9 L 28 9 L 28 5 L 28 4 L 27 4 L 23 4 z M 14.929688 10 L 14.929688 11 L 20.292969 11 L 12.453125 18.837891 L 13.162109 19.546875 L 21 11.707031 L 21 17.070312 L 22 17.070312 L 22 11.414062 L 22 10 L 14.929688 10 z M 4 11 L 4 15 L 5 15 L 5 11 L 4 11 z M 27 11 L 27 15 L 28 15 L 28 11 L 27 11 z M 4 17 L 4 20 L 5 20 L 5 17 L 4 17 z M 27 17 L 27 21 L 28 21 L 28 17 L 27 17 z M 4 21 L 4 23 L 4 28 L 9 28 L 11 28 L 11 21 L 4 21 z M 5 22 L 10 22 L 10 27 L 9 27 L 5 27 L 5 23 L 5 22 z M 27 23 L 27 27 L 23 27 L 23 28 L 28 28 L 28 23 L 27 23 z M 12 27 L 12 28 L 15 28 L 15 27 L 12 27 z M 17 27 L 17 28 L 21 28 L 21 27 L 17 27 z "
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['zoom_in']='ZoomIn'
    tooltips['zoom_in']='zoom in'
    UInames['zoom_in']=['zoomin','ZoomInMenu']


    svgs['zoom_out'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
       d="M 4 4 L 4 5 L 4 16 L 5 16 L 5 5 L 27 5 L 27 27 L 16 27 L 16 28 L 27 28 L 28 28 L 28 5 L 28 4 L 4 4 z M 23.837891 7.453125 L 16 15.292969 L 16 9.9296875 L 15 9.9296875 L 15 15.585938 L 15 17 L 22.070312 17 L 22.070312 16 L 16.707031 16 L 24.546875 8.1621094 L 23.837891 7.453125 z M 4 18 L 4 22 L 5 22 L 5 19 L 8 19 L 8 18 L 5 18 L 4 18 z M 10 18 L 10 19 L 13 19 L 13 22 L 14 22 L 14 19 L 14 18 L 13 18 L 10 18 z M 4 24 L 4 27 L 4 28 L 8 28 L 8 27 L 5 27 L 5 24 L 4 24 z M 13 24 L 13 27 L 10 27 L 10 28 L 14 28 L 14 24 L 13 24 z "
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['zoom_out']='ZoomOut'
    tooltips['zoom_out']='zoom out'
    UInames['zoom_out']=['zoomout','ZoomOutMenu']


    svgs['application_exit'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
 <g fill="#da4453" transform="translate(-384.57-515.8)">
  <path d="m388.57 519.8v24h24v-24zm1 6h22v17h-22z"/>
  <path d="m396.57 532.8h8v3h-8z"/>
 </g>
</svg>
    """
    callbacks['application_exit']='Quit'
    tooltips['application_exit']='quit'
    UInames['application_exit']=['application_exit','QuitMenu']


    svgs['document_open'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
       d="m4 4v24h24l-1-1h-22v-13h5l3-3h14v16l1 1v-21h-10l-3-3z"
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['document_open']='Open'
    tooltips['document_open']='open image'
    UInames['document_open']=['document_open','OpenMenu']


    svgs['document_save'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs
     id="defs3051">
    <style
       type="text/css"
       id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
  <path
     style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 4 4 L 4 28 L 9 28 L 23 28 L 28 28 L 28 10 L 27 9 L 23 5 L 22 4 L 21 4 L 10 4 L 4 4 z M 5 5 L 10 5 L 10 13 L 21 13 L 21 5 L 21.585938 5 L 27 10.414062 L 27 27 L 23 27 L 23 19 L 9 19 L 9 27 L 5 27 L 5 5 z M 11 5 L 17 5 L 17 12 L 11 12 L 11 5 z M 10 20 L 22 20 L 22 27 L 10 27 L 10 20 z "
     id="path60"
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['document_save'] ='Export'
    tooltips['document_save'] ='export image'
    UInames['document_save']=['document_save','ExportMenu']

    svgs['document_save_as'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs
     id="defs3051">
    <style
       type="text/css"
       id="current-color-scheme">
      .ColorScheme-Text {
        color:#4d4d4d;
      }
      </style>
  </defs>
  <path
     style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 4 4 L 4 28 L 15 28 L 15 27 L 10 27 L 10 20 L 18 20 L 18 19 L 9 19 L 9 27 L 5 27 L 5 5 L 10 5 L 10 13 L 21 13 L 21 5 L 21.585938 5 L 27 10.414062 L 27 16 L 28 16 L 28 10 L 22 4 L 10 4 L 4 4 z M 11 5 L 17 5 L 17 12 L 11 12 L 11 5 z M 24.398438 16 L 19.287109 21.111328 L 16 24.398438 L 16 28 L 19.601562 28 L 28 19.601562 L 24.398438 16 z M 22.349609 19.490234 L 24.509766 21.650391 L 21.335938 24.824219 L 21.335938 24.150391 L 20.322266 24.173828 L 19.287109 24.173828 L 19.287109 23.136719 L 19.287109 22.552734 L 22.349609 19.490234 z M 18.273438 23.564453 L 18.273438 25.185547 L 20.300781 25.185547 L 20.322266 25.839844 L 19.240234 26.919922 L 17.800781 26.919922 L 17.080078 26.199219 L 17.080078 24.757812 L 18.273438 23.564453 z "
     id="path76"
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['document_save_as'] = 'ExportAs'
    tooltips['document_save_as'] = 'export image as'
    UInames['document_save_as']=['document_save_as','ExportAsMenu']

    svgs['apply'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 19.292969 6 L 8.8535156 16.566406 L 4.7070312 12.369141 L 4 13.083984 L 8.1464844 17.28125 L 8.1445312 17.285156 L 8.8515625 18 L 8.8535156 17.998047 L 8.8554688 18 L 9.5625 17.285156 L 9.5605469 17.28125 L 20 6.7148438 L 19.292969 6 z "
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['apply'] = 'apply'
    tooltips['apply'] = 'apply'
    UInames['apply']=[]


    svgs['cancel'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 12 4 C 9.972402 4 8.12868 4.756694 6.71875 6 C 6.592511 6.11132 6.46272 6.22478 6.34375 6.34375 L 6 6.71875 C 4.756694 8.12868 4 9.972402 4 12 C 4 16.41828 7.58172 20 12 20 C 14.027598 20 15.87132 19.243306 17.28125 18 L 17.65625 17.65625 C 17.77522 17.53728 17.88868 17.407489 18 17.28125 C 19.243306 15.87132 20 14.027598 20 12 C 20 7.58172 16.41828 4 12 4 z M 12 5 C 15.86599 5 19 8.13401 19 12 C 19 13.75366 18.346785 15.334268 17.28125 16.5625 L 7.4375 6.71875 C 8.665731 5.653215 10.24634 5 12 5 z M 6.71875 7.4375 L 16.5625 17.28125 C 15.334268 18.346785 13.75366 19 12 19 C 8.13401 19 5 15.86599 5 12 C 5 10.24634 5.653215 8.665731 6.71875 7.4375 z "
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['cancel']='cancel'
    tooltips['cancel']='cancel'
    UInames['cancel']=[]


    svgs['close'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      .ColorScheme-NegativeText {
        color:#da4453;
      }
      </style>
  </defs>
  <path
     style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 12 4 A 8 8.00001 0 0 0 4 12 A 8 8.00001 0 0 0 12 20 A 8 8.00001 0 0 0 20 12 A 8 8.00001 0 0 0 12 4 z M 8.7070312 8 L 12 11.292969 L 15.292969 8 L 16 8.7070312 L 12.707031 12 L 16 15.292969 L 15.292969 16 L 12 12.707031 L 8.7070312 16 L 8 15.292969 L 11.292969 12 L 8 8.7070312 L 8.7070312 8 z "
     class="ColorScheme-NegativeText"
     />
</svg>
    """
    callbacks['close']='myclose'
    tooltips['close']='close'
    UInames['close']=[]


    svgs['ok'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 19.292969 6 L 8.8535156 16.566406 L 4.7070312 12.369141 L 4 13.083984 L 8.1464844 17.28125 L 8.1445312 17.285156 L 8.8515625 18 L 8.8535156 17.998047 L 8.8554688 18 L 9.5625 17.285156 L 9.5605469 17.28125 L 20 6.7148438 L 19.292969 6 z "
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['ok'] = 'ok'
    tooltips['ok'] = 'ok'
    UInames['ok']=[]


    svgs['preferences'] = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs id="defs3051">
    <style type="text/css" id="current-color-scheme">
      .ColorScheme-Text {
        color:#000000;
      }
      </style>
  </defs>
 <path style="fill:currentColor;fill-opacity:1;stroke:none"
     d="M 12.5 4 C 11.286139 4 10.280978 4.8559279 10.050781 6 L 4 6 L 4 7 L 10.050781 7 C 10.280978 8.1440721 11.286139 9 12.5 9 C 13.713861 9 14.719022 8.1440721 14.949219 7 L 20 7 L 20 6 L 14.949219 6 C 14.719022 4.8559279 13.713861 4 12.5 4 z M 6.5 15 C 5.1149999 15 4 16.115 4 17.5 C 4 18.885 5.1149999 20 6.5 20 C 7.7138604 20 8.7190222 19.144072 8.9492188 18 L 20 18 L 20 17 L 8.9492188 17 C 8.7190223 15.855928 7.7138604 15 6.5 15 z M 6.5 16 C 7.3310001 16 8 16.669 8 17.5 C 8 18.331 7.3310001 19 6.5 19 C 5.6689999 19 5 18.331 5 17.5 C 5 16.669 5.6689999 16 6.5 16 z "
     class="ColorScheme-Text"
     />
</svg>
    """
    callbacks['preferences'] = 'preferences'
    tooltips['preferences'] = 'preferences'
    UInames['preferences']=['ConfigMenu']

#
# end scribbleicons class
#

def svg_string_to_image(svg,scale):
    '''
    Transform a svg string into an image at a certain scale.
    '''
    loader = GdkPixbuf.PixbufLoader()
    loader.write(svg.encode())
    loader.close()
    pixbuf = loader.get_pixbuf()
    pixbuf = pixbuf.scale_simple(pixbuf.get_width()*iconSize/pixbuf.get_height()*scale, iconSize*scale, GdkPixbuf.InterpType.BILINEAR)
#   transform white background into transparent background
    transparent=pixbuf.add_alpha (True, 0xff, 0xff, 0xff)
    image=Gtk.Image.new_from_pixbuf(transparent)

    return image

def setup_UI():
    '''
    Theme the icons to our icon set, set the toolbar items' tooltips and their callbacks
    '''
    icon_factory=scribbleicons
    for icon in icon_factory.svgs.keys():
#       go over the icons
        if len(icon_factory.UInames[icon])>0:
#           but only the ones that have a nonempty corresponding UInames list
            for name in icon_factory.UInames[icon]:
#               go over the UInames, get the UIobject
                UIobject=builder.get_object(name)

                if isinstance(UIobject,gi.overrides.Gtk.ToolButton):
#                   Work on the toolbar items
                    img=svg_string_to_image(icon_factory.svgs[icon],12)
                    UIobject.set_icon_widget(img)
                    UIobject.set_tooltip_text(icon_factory.tooltips[icon])
                    UIobject.connect("clicked", getattr(Handler,icon_factory.callbacks[icon]))

                else:
#                   work on the menuitems
                    img=svg_string_to_image(icon_factory.svgs[icon],9)
                    UIobject.set_image(img)


def set_scrolled_window_to_coords(x,y,centered=True):
    '''
    Center scrolled window to the coordinates (x,y) given as argument
    '''
    if centered:
        cent=1
    else:
        cent=0
#   get info on the scrolling window adjustments
    hadj=scrolledwindow.get_hadjustment ()
    vadj=scrolledwindow.get_vadjustment ()
    (h_upper, h_page_size) = (hadj.get_upper(), hadj.get_page_size())
    (v_upper, v_page_size) = (vadj.get_upper(), vadj.get_page_size())
#   compute the new adjustments
    if x+cent*h_page_size/2<original_image.width*drawing_status.scale:
        newh = max(x-cent*h_page_size/2,0)
    else:
        newh=h_upper-h_page_size    
    if y+cent*v_page_size/2<original_image.height*drawing_status.scale:
        newv = max(y-cent*v_page_size/2,0)
    else:
        newv=v_upper-v_page_size        
#   set the adjustments to their new value        
    hadj.set_value (newh)        
    vadj.set_value (newv)



def inc_scrolled_window (adj,direction):
    '''Slow scroll (using arrow keys)'''
    (upper, page_size) = (adj.get_upper(), adj.get_page_size())
    newh = min(max(adj.get_value()+direction*(upper-page_size)/20,0),upper-page_size)
    adj.set_value (newh)


def scroll_page (adj,direction):
    '''Fast scroll (using PgUp and PgDn keys)'''
    (upper, page_size) = (adj.get_upper(), adj.get_page_size())
    newh = min(max(adj.get_value()+direction*page_size*0.8,0),upper-page_size)
    adj.set_value (newh)

def set_adj_to_max(adj):
    '''Set an adjustment to its maximum value (scroll to end)'''
    (upper, page_size) = (adj.get_upper(), adj.get_page_size())
    adj.set_value (upper - page_size)

def set_adj_to_min(adj):
    '''Set an adjustment to its minimum value (scroll to beginning)'''
    adj.set_value (adj.get_lower())

def scroll_to_corner(which):
    '''Scroll our drawing area to any of its four corners'''
    hadj = scrolledwindow.get_hadjustment()
    vadj = scrolledwindow.get_vadjustment()

    if (which == 'northwest'):
        set_adj_to_min (hadj)
        set_adj_to_min (vadj)

    elif (which=='northeast'):
        set_adj_to_max (hadj)
        set_adj_to_min (vadj)

    elif (which=='southeast'):
        set_adj_to_max (hadj)
        set_adj_to_max (vadj)

    elif (which=='southwest'):
        set_adj_to_min (hadj)
        set_adj_to_max (vadj)
#
#       end scrolling functions
#

class Handler:
    '''
    Class containing all the methods that get called from the UI
    '''

    def Quit(self, *args):
        '''Exit function'''
        Gtk.main_quit()

    def slider_changed(self,*args):
        '''React to a change in one of the three sliders'''
        allpaths.set_current_path_values_from_adjustments()
        allpaths.reset_predicted_point()
        drawingarea.queue_draw()

    def ToggleAutoScroll(self,*args):
        '''React to toggling of the autoscroll menubutton'''
        drawing_status.toggle_autoscroll()

    def ToggleClosestPoint(self,*args):
        '''React to toggling of the useclosestpoint menubutton'''
        drawing_status.toggle_closest()

    def autoadjust_toggle(self,*args):
        '''React to toggling of autoadjust points when moving'''
        drawing_status.toggle_autoadjustpoints()

    def open_toggle(x):
        '''React to clicking on "open path" toolbar button or the "o" key'''
        allpaths.set_current_path_open()
#       start new path
        allpaths.newpath()
#       reset drawing status, update toolbar
        drawing_status.initialize()
        update_toolbar()
        drawingarea.queue_draw()

    def closed_toggle(x):
        '''React to clicking on "closed path" toolbar button or the "c" key'''
        allpaths.set_current_path_closed()
#       start new path
        allpaths.newpath()
#       reset drawing status, update toolbar
        drawing_status.initialize()
        update_toolbar()
        drawingarea.queue_draw()


    def draw_mode_toggle(x):
        '''React to clicking on "draw mode" toolbar button'''
        if drawing_status.DrawMode:
            drawing_status.set_default_colormode()
        else:
            drawing_status.set_default_drawmode()
            
        update_toolbar()
        drawingarea.queue_draw()

    def color_mode_toggle(x):
        '''React to clicking on "color" toolbar button'''
        if drawing_status.ColorMode:
            drawing_status.set_default_drawmode()
        else:
            drawing_status.set_default_colormode()

        update_toolbar()
        drawingarea.queue_draw()

    def move_toggle(x):
        '''React to clicking on "move mode" toolbar button'''
        drawing_status.set_to_movemode()
        update_toolbar()
        drawingarea.queue_draw()


    def add_toggle(x):
        '''React to clicking on "add mode" toolbar button'''
        drawing_status.set_to_addmode()
        update_toolbar()
        drawingarea.queue_draw()


    def delete_toggle(x):
        '''React to clicking on "delete mode" toolbar button'''
        drawing_status.set_to_deletemode()
        update_toolbar()
        drawingarea.queue_draw()

    def white_toggle(x):
        '''React to clicking on "white mode" toolbar button'''
        drawing_status.set_to_whitemode()
        update_toolbar()
        drawingarea.queue_draw()

    def black_toggle(x):
        '''React to clicking on "black mode" toolbar button'''
        drawing_status.set_to_blackmode()
        update_toolbar()
        drawingarea.queue_draw()

    def select_mode_toggle(x):
        '''React to clicking on "select path mode" toolbar button'''
        drawing_status.toggle_selectmode()
        update_toolbar()
        drawingarea.queue_draw()

    def Export(self,*args):
        '''React to the Export call'''
        allpaths.export(original_image.pdf_file)

    def ExportAs(self,*args):
        '''React to the Export As call'''
#       setup the "export as" window dialog 
        dialog = Gtk.FileChooserDialog(title="Choose a pdf to export to",parent=window,
             action=Gtk.FileChooserAction.SAVE,
             do_overwrite_confirmation=True)
#       add a cancel button 
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
#       and an "export as" button for when a file is selected
        dialog.add_button('export as', Gtk.ResponseType.OK)
#       suggest the usual name to export to 
        dialog.set_current_name(original_image.pdf_file)
#       filter to only display pdf files
        filter_pdf = Gtk.FileFilter()
        filter_pdf.set_name("pdf files")
        filter_pdf.add_mime_type("application/pdf")
        dialog.add_filter(filter_pdf)        
#       run the dialog
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename=dialog.get_filename()
#       clear the dialog
        dialog.destroy()        
        if response == Gtk.ResponseType.OK:            
            original_image.set_pdf_file(filename)
            allpaths.export(original_image.pdf_file)

    def Open(self,*args):
        '''React to the Open call'''
#       setup the "open" window dialog 
        dialog = Gtk.FileChooserDialog(title="Choose image",parent=window,
             action=Gtk.FileChooserAction.OPEN)
#       add a cancel button 
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
#       and an open button for when a file is selected
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
#       filter to only display pdf files
        filter_png = Gtk.FileFilter()
        filter_png.set_name("png files")
        filter_png.add_mime_type("image/png")
        dialog.add_filter(filter_png)        
#       run the dialog
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename=dialog.get_filename()

#       clear the dialog
        dialog.destroy()        
        if response == Gtk.ResponseType.OK:            
            original_image.open_file(filename)
            drawingarea.queue_draw()

    def cairo_draw(self,drawingarea,context):
        '''React to the drawingarea.queue_draw signal'''
        context.scale(drawing_status.scale,drawing_status.scale)
        context.set_source_surface(original_image.surface,0,0)
        context.paint()
        allpaths.draw_all(context,withpoints=True)
        return False

    def Config(self,*args):
        '''React to the Config menuitem'''
        scribblesettingswindow.show_all()

    def hide_window(self,window,*args):
        '''Hide the window given as parameter'''
        window.hide()
        return True

    def destroy(self,window,*args):
        '''react to the destroy event'''
        print('destroy!!')
#        window.hide()
        return True


    def ColorPicker(self,*args):
        '''React to the Color Picker menuitem'''
        print('TODO: ColorPicker')        
        
        if builder.get_object('UseLegacyColorPickerMenu').get_active():
#            ColorSelectionLegacy=builder.get_object('ColorSelectionLegacy')
#           get the color from a "pick" (keypress p + click on image)
#           or from the current active color
#            ColorSelectionLegacy.get_color_selection().set_current_rgba(color)
#            ColorSelectionLegacy.show()
            dialog=Gtk.ColorSelectionDialog(title='pick a color')
            dialog.set_transient_for(window)            
            response=dialog.run()
            if response == Gtk.ResponseType.OK:
                print(dialog.get_color_selection().get_current_rgba())
            elif response == Gtk.ResponseType.CANCEL:
                print('color pick canceled')
            dialog.destroy()
        else:
#           get the color from a "pick" (keypress p + click on image)
#           or from the current active color
#            builder.get_object('ColorSelectionWidget').set_rgba(color)
#            builder.get_object('ColorSelectionWidget').set_property("show-editor", False)
#            builder.get_object('ColorSelectionWindow').show()
            
            dialog=Gtk.ColorChooserDialog(title='pick a color')
            dialog.set_transient_for(window)            
            response=dialog.run()
            if response == Gtk.ResponseType.OK:
                print(dialog.get_rgba())
            elif response == Gtk.ResponseType.CANCEL:
                print('color pick canceled')            
            dialog.destroy()

    def ZoomIn(self,*args):
        '''React to the Zoom In menuitem, or the "+" key or the ctrl+scroll'''
        drawing_status.increase_scale()
        drawingarea.set_size_request (original_image.width*drawing_status.scale,original_image.height*drawing_status.scale)
        drawingarea.queue_draw()

    def ZoomOut(self,*args):
        '''React to the Zoom Out menuitem, or the "-" key or the ctrl+scroll'''
        drawing_status.decrease_scale()
        drawingarea.set_size_request (original_image.width*drawing_status.scale,original_image.height*drawing_status.scale)
        drawingarea.queue_draw()

    def mouse_scroll_event(self, widget, event):
        '''handles mouse scroll events'''        
        # Handles zoom in / zoom out on Ctrl+mouse wheel
#        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
#        if ctrl == Gdk.ModifierType.CONTROL_MASK:
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            hadj=scrolledwindow.get_hadjustment()
            vadj=scrolledwindow.get_vadjustment()
#           get the scroll point in "natural" coordinates (=coordinates in the original pic)
            scroll_point=point(hadj.get_value(),vadj.get_value())
#           get the event in "natural" coordinates
            newpoint=point(event)
#           get the direction of the scroll
            direction = event.get_scroll_deltas()[2]
#           keep track of the old scale
            old_scale=drawing_status.scale
#           change the scale, redraw
            if direction > 0:
                self.ZoomOut()
            else:
                self.ZoomIn()

            if newpoint.isvalid:
#               delta of the scaling adjustment
                factor=(drawing_status.scale/old_scale)-1
#               coordinates of the new scrolling point, expressed in the (new) scrolling window scale
                x=(scroll_point.x+(newpoint.x-scroll_point.x)*factor)*drawing_status.scale
                y=(scroll_point.y+(newpoint.y-scroll_point.y)*factor)*drawing_status.scale
                set_scrolled_window_to_coords(x,y,centered=False)

#           do not propagate event, as we have handled the zoom scrolling ourselves
            return True
        else:
#           propagate the event so the scrolling window scrolls ;-)
            return False
        
    def button_release_event(self,window,event):
        pass

    def button_press_event(self,window,event):
        '''React to clicks'''
#       set newpoint corresponding to event 
        newpoint=point(event)        
        if newpoint.isvalid:
#           our point is inside the picture, and not too close to the last valid point 

            if drawing_status.AutoScroll:
                set_scrolled_window_to_coords(event.x,event.y)
#           is this a point we have already met?            
            path_selected=allpaths.get_current_path_and_position_values(newpoint)
            if path_selected and drawing_status.ClosestPoint:
#               replace point with closest existing point found in our path(s) if one is close enough                
                newpoint=allpaths.current_point

            if allpaths.predicted_point is not None and newpoint.space_distance(allpaths.predicted_point)<drawing_constants.mindistance:
#               newpoint is close to predicted point, replace it
                newpoint=allpaths.predicted_point

            if allpaths.adjusted_point is not None and newpoint.space_distance(allpaths.adjusted_point)<drawing_constants.mindistance:
#               newpoint is close to adjusted point, replace it              
                newpoint=allpaths.adjusted_point
                        
            if event.button==1:
#               we react to left clicks                             
                if not drawing_status.SelectPathMode:
                    # we are not selecting path (=> we are adding a point, 
                    # or dropping a previously selected point for moving)                
                    if drawing_status.AddMode:
                        # we are in addmode
                        allpaths.add_point_to_current_path(newpoint)                    
                    elif drawing_status.MoveMode:
                        # we are in movemode
                        allpaths.replace_point_in_current_path(newpoint)
                        # go back to select path mode 
                        drawing_status.toggle_selectmode()
                        update_toolbar()
    
    
                elif drawing_status.SelectPathMode and path_selected:        
                    # we are in select path mode, so we are 
#                        1) coloring paths or 
#                        2) deleting points 
#                        3) selecting a point for adding after or moving
                    if drawing_status.ColorMode:
                        # set corresponding color
                        if drawing_status.BlackMode:
                            allpaths.mark_current_path_segment_black()
                        else:
                            allpaths.mark_current_path_segment_transparent()
                        
                    if drawing_status.DeleteMode:
                        allpaths.delete_point_from_current_path()
                    
                    if not (drawing_status.DeleteMode or drawing_status.ColorMode):
                        # if we are not in DeleteMode nor ColorMode and we found a path/position (path_selected above is true), 
                        # we do not need to be selecting path anymore
                        drawing_status.toggle_selectmode()
                        update_toolbar()

            if event.button==3:
                print('TODO: set button 3 as eraser?')
#           we have consumed the adjusted point and/or the predicted point above, so we can forget about them
#           in any case, the queue_draw call below will recompute them if we are in the appropriate mode
            allpaths.reset_adjusted_point()
            allpaths.reset_predicted_point()
#           redraw the paths, reflecting the changes made above
            drawingarea.queue_draw()

    def KeyPressHandler(self,window,event):
        '''React to key presses'''
        key_val=event.keyval

#        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)        
#        if ctrl == Gdk.ModifierType.CONTROL_MASK:
        if event.state & Gdk.ModifierType.CONTROL_MASK:
#           we are not catching ctrl+key events here, but we could at a later stage
            return False

        if (key_val == Gdk.KEY_Escape) or (key_val == Gdk.KEY_q):
#           quit on esc or q 
            self.Quit()

        if key_val == Gdk.KEY_c:
#           mark current path as closed, start new one
            self.closed_toggle()
            return True

        if key_val == Gdk.KEY_f:
#           cycle through the fillcolors 
            allpaths.increase_fill_color_in_current_path()
            drawingarea.queue_draw()
            return True

        if key_val == Gdk.KEY_o or key_val == Gdk.KEY_n:
#           mark the current path as open, start new one
            self.open_toggle()
            return True

        if key_val == Gdk.KEY_p:
#           replace current point by predicted one 
            allpaths.set_current_to_predicted_point()
            drawingarea.queue_draw()


        if key_val == Gdk.KEY_a:
#           replace current point by adjusted one             
            allpaths.set_current_to_adjusted_point()
            drawingarea.queue_draw()

        if key_val == Gdk.KEY_Right:
#           horizontal scrolling on arrow key 
            adj = scrolledwindow.get_hadjustment()
            inc_scrolled_window(adj,1);
            return True

        if key_val == Gdk.KEY_Up:
#           verticak scrolling on arrow key            
            adj = scrolledwindow.get_vadjustment ()
            inc_scrolled_window(adj,-1)
            return True

        if key_val == Gdk.KEY_Down:
#           vertical scrolling on arrow key            
            adj = scrolledwindow.get_vadjustment ()
            inc_scrolled_window(adj,1)
            return True

        if key_val == Gdk.KEY_Left:
#           horizontal scrolling on arrow key            
            adj = scrolledwindow.get_hadjustment ()
            inc_scrolled_window(adj,-1)
            return True

        if key_val == Gdk.KEY_Page_Up:
#           fast vertical scrolling on page up key            
            adj = scrolledwindow.get_vadjustment ()
            scroll_page(adj,-1)
            return True

        if key_val == Gdk.KEY_Page_Down:
#           fast vertical scrolling on page down key                        
            adj = scrolledwindow.get_vadjustment ()
            scroll_page(adj,1)
            return True

        if key_val == Gdk.KEY_plus or key_val == Gdk.KEY_KP_Add:                        
#           zoom in on + key 
            self.ZoomIn()
            return True

        if key_val == Gdk.KEY_minus or key_val == Gdk.KEY_KP_Subtract:
#           zoom out on + key            
            self.ZoomOut()
            return True

        
        if key_val == Gdk.KEY_1 or key_val == Gdk.KEY_Home:
            # key=1=northwest corner adjustment
            scroll_to_corner('northwest')
            return True
        
        if key_val == Gdk.KEY_2:
            # key=2=northeast corner adjustment
            scroll_to_corner('northeast');
            return True

        
        if key_val == Gdk.KEY_3 or key_val == Gdk.KEY_End:
            # key=3=southeast corner adjustment
            scroll_to_corner('southeast')
            return True
        
        if key_val == Gdk.KEY_4:
            # key=4=southwest corner adjustment
            scroll_to_corner('southwest')
            return True

        if key_val == Gdk.KEY_parenleft or key_val == Gdk.KEY_parenright:
            # mark current path as Bezier curve
            allpaths.set_current_path_as_Bezier()
            drawingarea.queue_draw()
            return True

        if key_val == Gdk.KEY_bracketleft or key_val == Gdk.KEY_bracketright:
            # mark current path as polygon (=non Bezier)
            allpaths.set_current_path_as_Polygon()
            drawingarea.queue_draw()
            return True

        # set next segment as black
        if key_val == Gdk.KEY_b: 
            if drawing_status.MoveMode:
                allpaths.currentposition+=1            
            allpaths.mark_current_path_segment_black()            
            if drawing_status.MoveMode:
                allpaths.currentposition-=1            
            drawingarea.queue_draw()
            return True

        # set next segment as white
        if key_val == Gdk.KEY_w:            
            if drawing_status.MoveMode:
                allpaths.currentposition+=1
            allpaths.mark_current_path_segment_transparent()            
            if drawing_status.MoveMode:
                allpaths.currentposition-=1            
            drawingarea.queue_draw()
            return True

    def reset_slider_values(self,*args):
        '''Reset our sliders to their default values'''
        circleradiusadjustment.set_value(150)
        sectoropeningadjustment.set_value(30)
        linewidthadjustment.set_value(32)
        drawingarea.queue_draw()
        return True

#
# end Handler class
#



class status(object):

    def __init__(self):
        '''class initialization'''
        self.initialize()

    def initialize(self):
        '''Initial status mode. We want to draw an open path, in black, adding points to a new path (hence not SelectPathMode)'''
        self.DrawMode=True
        self.ColorMode=False
        self.OpenPath=True
        self.ClosedPath=False
        self.AddMode=True
        self.MoveMode=False
        self.DeleteMode=False
        self.SelectPathMode=False
        self.BlackMode=True
        self.WhiteMode=False
        self.AutoScroll=True
        self.AutoScroll=AutoScroll.get_active()
        self.ClosestPoint=UseClosestPoint.get_active()
        self.AutoAdjustPoints=AutoAdjustPoints.get_active()
        self.scale=1
        self.last_valid_point=None

    def set_last_valid_point(self,point):
        '''set last valid point to point'''
        self.last_valid_point=point

    def set_default_drawmode(self):
        '''Mode obtained when clicking on the "add point" toolbar UI. Same as init mode, but we want to select a path first'''
        self.DrawMode=True
        self.ColorMode=False
        self.AddMode=True
        self.MoveMode=False
        self.DeleteMode=False
        self.SelectPathMode=True

    def set_default_colormode(self):
        '''Mode obtained when clicking on the "Color Mode" selector. We want to mark the next segment as black, and it needs to be selected'''
        self.DrawMode=False
        self.ColorMode=True
        self.SelectPathMode=True
        self.BlackMode=True
        self.WhiteMode=False

    def set_to_addmode(self):
        '''Mode obtained when clicking on the "add mode" selector. We want to add a new point to an existing path, which needs to be selected'''
        self.AddMode=True
        self.MoveMode=False
        self.DeleteMode=False
        self.SelectPathMode=True

    def set_to_movemode(self):
        '''Mode obtained when clicking on the "move mode" selector. We want to move a point in an existing path, which needs to be selected'''
        self.AddMode=False
        self.MoveMode=True
        self.DeleteMode=False
        self.SelectPathMode=True

    def set_to_deletemode(self):
        '''Mode obtained when clicking on the "delete mode" selector. We want to delete a point to an existing path, which needs to be selected'''
        self.AddMode=False
        self.MoveMode=False
        self.DeleteMode=True
        self.SelectPathMode=True

    def set_to_blackmode(self):
        '''Mode obtained when clicking on the "black mode" selector. We want to mark a segment as black in an existing path, which needs to be selected'''
        self.BlackMode=True
        self.WhiteMode=False
        self.set_to_addmode()

    def set_to_whitemode(self):
        '''Mode obtained when clicking on the "white mode" selector. We want to mark a segment as white in an existing path, which needs to be selected'''
        self.BlackMode=False
        self.WhiteMode=True
        self.set_to_addmode()

    def toggle_selectmode(self):
        '''Flip the select mode'''
        self.SelectPathMode=not self.SelectPathMode

    def toggle_autoscroll(self):
        '''Set the autoscroll to the value of the AutoScroll radio button in the Settings menu'''
        self.AutoScroll=AutoScroll.get_active()

    def toggle_closest(self):
        '''Set the useclosestpoint to the value of the UseClosestPoint radio button in the Settings menu'''
        self.ClosestPoint=UseClosestPoint.get_active()

    def toggle_autoadjustpoints(self):
        '''Set the useclosestpoint to the value of the UseClosestPoint radio button in the Settings menu'''
        self.AutoAdjustPoints=AutoAdjustPoints.get_active()

    def increase_scale(self,slow=False):
        '''Increase the scale to obtain zoom in'''
        if slow:
            self.scale=self.scale*1.02
        else:
            self.scale=self.scale*1.1

    def decrease_scale(self,slow=False):
        '''Decrease the scale to obtain zoom out'''
        if slow:
            self.scale=self.scale/1.02
        else:
            self.scale=self.scale/1.1

    def set_scale(self,scale):
        '''Set the scale value'''
        self.scale=scale

#
# end status class
#


class constants(object):

    def __init__(self):
        '''initialization of the constants class'''
        self.set_from_image()

    def set_from_image(self):
        '''set the drawing constants from the original image'''
        self.circleradius=circleradiusadjustment.get_value()    # radius of sector/circle for prediction
        self.sectoropening=sectoropeningadjustment.get_value()  # (half-)opening of sector for prediction

        value=linewidthadjustment.get_value()/100
        value=0.1+2*value+8*value**3;
#       main linewidth params
        self.millimeter_width=0.9*value             # linewidth in millimeters (for a 2350 pixel wide image)

#       set the constants that are derived from millimeter_width
        self.set_derived()

    def set_derived(self):
        '''Set the constants that are dependent from millimeter_width'''
        self.linewidth=self.millimeter_width*original_image.width/210
        self.pointrad=self.linewidth/4

        self.longirange = self.linewidth    # in auto-adjust: width of weight support in direction tangent to path (Gaussian weight<0.1 outside range)
        self.latirange  = self.linewidth    # in auto-adjust: width of weight support in direction perpend to path (weight=0 outside range)

#       in "closest" mode, will replace current point by any (other) existing point whose distance is less than this:
        self.minclosestdistance=self.linewidth
        self.mindistance=self.linewidth

    def set_from_path(self,path):
        '''set the drawing constants from a path'''
#       load the defaults
        self.set_from_image()
#       set from path
        self.circleradius=path.circleradius
        self.sectoropening=path.sectoropening

        value=path.linewidth/100
        value=0.1+2*value+8*value**3;
#       main linewidth params
        self.millimeter_width=0.9*value             # linewidth in millimeters (for a 2350 pixel wide image)
#       set the parameters that are derived from millimeter_width
        self.set_derived()

#
# end constants class
#

class point(object):

    def __init__(self,*args,**kwargs):
        '''point initialization'''
#       take care of the various types of non named arguments tuple (x,y), numpy array or event
        if isinstance(args[0],numpy.ndarray):
            args=args[0]
            if args.shape[0]==1:
                args=args[0]

        if isinstance(args[0],gi.overrides.Gdk.EventScroll) or isinstance(args[0],gi.overrides.Gdk.EventButton):
            args=[args[0].x,args[0].y]

        x=args[0]
        y=args[1]
#       take care of the named arguments
        if 'do_scaling' in kwargs.keys():
            do_scaling=kwargs['do_scaling']
        else:
            do_scaling=True

        self.isvalid=False
        if do_scaling:
#           convert coordinates to "natural" ones (division by scale, to get coords relative to original image scale) 
            self.coords=numpy.array([[x/drawing_status.scale,y/drawing_status.scale]])
        else:
            self.coords=numpy.array([[x,y]])

        self.time=datetime.datetime.now()
#       keep track separately of both coordinates
        self.x=self.coords[0,0]
        self.y=self.coords[0,1]
        if self.x>=0 and self.x<=original_image.width and self.y>=0 and self.y<=original_image.height:
#           point is inside the original image
            self.isvalid=True

        if self.isvalid:
            if drawing_status.last_valid_point is not None:
#               check its distance to our last valid point
                distance_to_last_valid_point=self.space_time_distance(drawing_status.last_valid_point)

                if distance_to_last_valid_point>drawing_constants.mindistance:
#                   this point was not recently used (or is far from the last one used)
                    drawing_status.set_last_valid_point(self)
                else:
#                   point is too close to the last valid one, reject it
                    self.isvalid=False
            else:
#               last valid point does not exist (yet), so we set it to the current one
                drawing_status.set_last_valid_point(self)

    def space_time_distance(self,point):
        '''compute the (space-time) distance between self and point'''
        return ((self.x-point.x)**2+(self.y-point.y)**2+((self.time-point.time).total_seconds()/0.5*drawing_constants.mindistance)**2)**0.5

    def space_distance(self,point):
        '''compute the (space-time) distance between self and point'''
        return ((self.x-point.x)**2+(self.y-point.y)**2)**0.5


    def replace_with_weighted_average(self,tangent_vector):
        '''replace coordinates with a local weighted average'''
        u=tangent_vector[0]
        v=tangent_vector[1]
#       center of the weighted average
        rX=self.x
        rY=self.y
#       how far arount of the center to look for points. we take a square of side twice as big as the support of the cut functions
        delta=int(2*max(drawing_constants.latirange,drawing_constants.longirange))
#       corners of the region to be averaged, making sure it is inside the original image
        minX=max(int(rX)-delta,0)
        maxX=min(int(rX)+delta,original_image.width)+1
        minY=max(int(rY)-delta,0)
        maxY=min(int(rY)+delta,original_image.height)+1
#       slice of the coordinates matrix that correspond to the averaging region
        i=original_image.i[minX:maxX,minY:maxY]
        j=original_image.j[minX:maxX,minY:maxY]
#       slice of intensity matrix, multiplied with the cut functions, in the coordinate system of the tangent vector
        weight_matrix=original_image.intensity[minX:maxX,minY:maxY]*laticut((-v*(i-rX)+u*(j-rY)),drawing_constants.latirange)*longicut((u*(i-rX)+v*(j-rY)),drawing_constants.longirange)
#       average weight
        wei=sum(sum(weight_matrix))

        if wei>0:
#           there are non-zero intensity points in our region 
#           so we compute the averaged coordinates wrt to the weight matrix fac 
            mX=sum(sum(weight_matrix*i))/wei
            mY=sum(sum(weight_matrix*j))/wei
#           replace the point's coordinates with the averaged ones 
            self.x=mX
            self.y=mY
            self.coords=numpy.array([[mX,mY]])
#       keep track of the weight of the point
        self.weight=wei



    def average_nearby_color(self):
        '''Compute the average color of nearby points'''
        self.color=original_image.rgba_array[int(self.x),int(self.y),:]

    def __str__(self):
        self.average_nearby_color()
        return 'point coordinates: x={} y={} color={}'.format(self.x,self.y,self.color)

#
# end point class
#

#%%

class path(object):
    def __init__(self,line=None,linewidth=None,circleradius=None,sectoropening=None):
        '''path object initialization'''

        self.dirty=True
        self.is_Bezier=True
        self.is_closed=False
        self.fillcolor=0
        try:
            self.set_values_from_adjustments()
        except:

            if linewidth is None:
                self.linewidth=32
            else:
                self.linewidth=linewidth

            if circleradius is None:
                self.circleradius=150
            else:
                self.circleradius=circleradius

            if sectoropening is None:
                self.sectoropening=30
            else:
                self.sectoropening=sectoropening

        self.points=numpy.empty(shape=[0,2])
        self.colors=numpy.empty(shape=[0,])

        if line is not None:
            self.read_from_v1_string(line)

    def increase_fill_color(self):
        '''cycle through fillcolors'''
        self.fillcolor+=1
        if self.fillcolor==3:
            self.fillcolor=0

    def mark_dirty(self):
        '''mark path as dirty'''
        self.dirty=True

    def set_as_Bezier(self):
        '''mark the path as Bezier'''
        self.is_Bezier=True

    def set_as_Polygon(self):
        '''mark the path as Polygon (=non Bezier)'''
        self.is_Bezier=False

    def set_open(self):
        '''mark path as open'''
        self.is_closed=False
#       set dirty flag so the Bezier points are recomputed
        self.dirty=True

    def set_closed(self):
        '''mark path as closed'''
        if len(self.points)>2:
#           having a closed path of 1 or 2 points makes no sense (and is break things)
            self.is_closed=True
#           set dirty flag so the Bezier points are recomputed
            self.dirty=True

    def set_values_from_adjustments(self):
        '''set defaults value for constants from sliders'''
        self.circleradius=circleradiusadjustment.get_value()
        self.sectoropening=sectoropeningadjustment.get_value()
        self.linewidth=linewidthadjustment.get_value()

    def draw(self,context,currentflag=False,currentposition=0,withpoints=True,linewidth_scale=1):
        '''use a Cairo context to draw the path'''
#       set the drawing constants from the path
        drawing_constants.set_from_path(self)
        colors=self.colors

        points=self.points

        if len(points)==1:

            if withpoints:
                # there is only one point in our path
                context.set_source_rgba(1.0, 0.0, 0.0, 1)

                i=0
                # set the color according to the selectpath state
                if currentflag and (((i==currentposition) and drawing_status.MoveMode) or ((i==currentposition-1) and drawing_status.AddMode)) and (not drawing_status.SelectPathMode):
                  context.set_source_rgba(0.0, 0.0, 1.0, 1)
                else:
                  context.set_source_rgba(1.0, 0.0, 0.0, 1)

                #draw the point
                context.arc(points[i,0],points[i,1],3*drawing_constants.pointrad,0,2 * numpy.pi)
                context.fill()

            return

        context.set_source_rgba(0.0, 0.0, 0.0, 1)
        context.set_line_width(drawing_constants.linewidth*linewidth_scale)
        context.set_line_cap(cairo.LINE_CAP_ROUND);

        if self.dirty:
            self.compute_Bezier()

############################################ draw the path ############################################
        if self.is_closed:
#           if path is closed, add the first point at the end, so we come back to it to actually close the path.
            points=numpy.append(points,points[[0],:],axis=0)

        for i in range(len(points)-1):

            # if we are adding points inside an existing path (and not at the end), highlight the segment in green
            if withpoints and currentflag and (i==currentposition-1) and drawing_status.AddMode and not drawing_status.ColorMode and not drawing_status.SelectPathMode:
              context.set_source_rgba(0.0, 1.0, 0.0, 1);
            else:
              context.set_source_rgba(0.0, 0.0, 0.0, 1);

            # white segments are drawn in gray with half linewidth on screen (so we know where they are)
            context.set_line_width(drawing_constants.linewidth*linewidth_scale)
            color_position=i+1
            if color_position==len(colors):
                color_position=0
            if withpoints:                
                if colors[color_position]==0:
                    context.set_source_rgba(0.5, 0.5, 0.5, 1)
                    context.set_line_width(drawing_constants.linewidth*linewidth_scale/2)

            context.move_to(points[i,0],points[i,1])
            # draw a Bezier segment
            if colors[color_position]==1 or withpoints==1:

                if self.is_Bezier:
                    context.curve_to(self.first_control_points[i,0],self.first_control_points[i,1],self.second_control_points[i,0],self.second_control_points[i,1],points[i+1,0],points[i+1,1])
                else:
                    context.line_to(points[i+1,0],points[i+1,1])

                # we have to strike here because the color might change in between segments
                context.stroke()


############################################ end draw the path ############################################


############################################ fill the path ############################################
        if self.fillcolor>0:

            context.move_to(points[0,0],points[0,1])
            context.set_line_width(0)
            for i in range(len(points)-1):

                if self.is_Bezier:
                   context.curve_to(self.first_control_points[i,0],self.first_control_points[i,1],self.second_control_points[i,0],self.second_control_points[i,1],points[i+1,0],points[i+1,1])
                else:
                    context.line_to(points[i+1,0],points[i+1,1])

            context.close_path()
            if withpoints:
                # we draw on screen, so we set transparency to 1/2, white=lightgrey and black=darkgray
                if self.fillcolor==1:
                    context.set_source_rgba(0.3, 0.3, 0.3, 0.5)
                else:
                    context.set_source_rgba(0.7, 0.7, 0.7, 0.5)

            else:
                # we draw on pdf, so we set transparency to opaque, white=white and black=black
                if self.fillcolor==1:
                    context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
                else:
                    context.set_source_rgba(1.0, 1.0, 1.0, 1.0)

            context.fill()
############################################ end fill the path ############################################


############################################ add the points ############################################
        if withpoints:
#           we draw on screen, so we add points so we can identify them later (to move or delete, for instance)
            context.set_source_rgba(1.0, 0.0, 0.0, 1)
#           the "current" point is drawn in blue, but "current" index depends on whether the path is closed or not
            loccurrentpos=currentposition
            if drawing_status.MoveMode and (currentposition==0) and self.is_closed:
                loccurrentpos=len(points)-1

            if(drawing_status.AddMode) and (currentposition==1) and self.is_closed:
                loccurrentpos=len(points)

            for i in range(len(points)):


                if currentflag and (((i==loccurrentpos) and drawing_status.MoveMode) or ((i==loccurrentpos-1) and drawing_status.AddMode)) and not drawing_status.SelectPathMode:
                    context.set_source_rgba(0.0, 0.0, 1.0, 1)
                else:
                    context.set_source_rgba(1.0, 0.0, 0.0, 1)

#               draw point
                context.arc (points[i,0],points[i,1],3*drawing_constants.pointrad,0,2*numpy.pi)
                context.fill()

                # add a small white sector to indicate in which direction the path is growing
                # we use the Bezier "first" control points to know the tangent to the path at the given point

            context.set_source_rgba(1.0, 1.0, 1.0, 1)
#           watch out, if the path is closed, we added an extra point identical to the first, but there is no need to go there twice
            for i in range(len(points)-self.is_closed):
#               get the reversed-angle-with-x-axis of the (oriented) tangent to the path at point i
                angle=math.atan2(self.tangents[i,1],self.tangents[i,0])+numpy.pi;

                context.move_to(points[i,0],points[i,1])
                context.arc (points[i,0],points[i,1],3*drawing_constants.pointrad,angle-0.7,angle+0.7)
                context.fill()


############################################ end add the points ############################################

    def compute_Bezier(self):
        '''compute the Bezier control points'''
        if len(self.points)<=2:
#           if we arrive here with a path that has less than 3 points, we set it to open, and mark it as dirty
            if self.is_closed:
                self.is_closed=False
                self.dirty=True

        if self.dirty:
#           compute the control points
            points=self.points

            if len(points)==2:
                first  = numpy.zeros_like(points[1:,:],dtype=float)
                second = numpy.zeros_like(points[1:,:],dtype=float)
                first[0,:]=(2*points[0,:]+points[1,:])/3
                second[0,:]=2*first[0,:]-points[0,:]
            else:


                if not self.is_closed:

                    N=len(points)-1

                    OpenMatrix=numpy.eye(N,N,k=-1)+numpy.eye(N,N)*4+numpy.eye(N,N,k=1)
                    OpenMatrix[0,0]=2
                    OpenMatrix[N-1,N-1]=7
                    OpenMatrix[N-1,N-2]=2

                    RHS=numpy.zeros_like(points[1:,:],dtype=float)
                    RHS[0,:]=points[0,:]+2*points[1,:]
                    RHS[1:-1,:]=4*points[1:-2,:]+2*points[2:-1,:]
                    RHS[-1,:]=8*points[-2,:]+points[-1,:]

                    first=numpy.linalg.solve(OpenMatrix,RHS)
                    second=numpy.zeros_like(first,dtype=float)
                    second[0:-1,:]=2*points[1:-1,:]-first[1:,:]
                    second[-1,:]=(points[-1,:]+first[-1,:])/2


                else:
                    N=len(points)

                    ClosedMatrix=numpy.eye(N,N,k=-1)+numpy.eye(N,N)*4+numpy.eye(N,N,k=1)
                    ClosedMatrix[0,N-1]=1
                    ClosedMatrix[N-1,0]=1

                    RHS=numpy.zeros_like(points,dtype=float)
                    RHS[0:-1]=4*points[0:-1,:]+2*points[1:,:]
                    RHS[-1]=4*points[-1,:]+2*points[0,:]

                    first=numpy.linalg.solve(ClosedMatrix,RHS)
                    second=numpy.zeros_like(first,dtype=float)
                    second[0:-1,:]=2*points[1:,:]-first[1:,:]
                    second[-1,:]=2*points[0,:]-first[0,:]

            self.first_control_points=first
            self.second_control_points=second

#           unit tangent vectors to the path at each point
            tangents=numpy.zeros_like(points,dtype=float)
#           for the first N-1 points, we use the first control points
            tangents[0:len(points)-1,:]=first[0:len(points)-1,:]-points[0:len(points)-1,:]
#           and for the last point on the path, the second control point
            tangents[len(points)-1,:]=points[len(points)-1,:]-second[len(points)-2,:]
#           normalize by the length
            tangents=tangents/((tangents**2).sum(axis=1)**0.5).reshape(len(tangents),1)

            self.tangents=tangents

            self.dirty=False

    def mark_segment_black(self,position):
        '''mark segment at position as black'''
        if position==len(self.colors):
            position=0
        self.colors[position]=1

    def mark_segment_transparent(self,position):
        '''mark segment at position as transparent'''        
        if position==len(self.colors):
            position=0    
        self.colors[position]=0



    def add_point(self,point, position):
        '''add point at position in path'''
        self.points=numpy.insert(self.points,position,point.coords,0)
        if drawing_status.BlackMode:
            self.colors=numpy.insert(self.colors,position,1,0)
        else:
            self.colors=numpy.insert(self.colors,position,0,0)
#       set the dirty flag as the Bezier control points will need to be re-computed
        self.dirty=True

    def delete_point(self,position):
        '''delete point at position in path'''
        self.points=numpy.delete(self.points,position,0)
        self.colors=numpy.delete(self.colors,position,0)
        if len(self.points)<=2:
#           a path that has less than 3 points is open by definition
            if self.is_closed:
                self.is_closed=False
#       set the dirty flag as the Bezier control points will need to be re-computed
        self.dirty=True

    def replace_point(self,point,position):
        '''replace point at position'''
        self.points[position,:]=point.coords
#       set the dirty flag as the Bezier control points will need to be re-computed
        self.dirty=True

    def range_interval(self):
        '''Compute the range ([[min_x,min_y],[max_x,max_y]]) of the path coordinates'''
        range_interval=numpy.empty([2,2])
        range_interval[0,:]=self.points.min(axis=0)
        range_interval[1,:]=self.points.max(axis=0)

        return range_interval


    def isempty(self):
        '''test whether path is empty'''
        return len(self.points)==0

    def read_from_v1_string(self,line):
        '''read path from v1 (=perl) line string'''
        records={}
        for element in line.split('$'):
            if '=' in element:
                element=element.replace(';','')
                pair=element.split('=')
                if 'pathX=' in element or 'pathY=' in element:
                    records[pair[0]]=[float(x) for x in pair[1].replace('[','').replace(']','').replace(' ','').split(',')]
                elif 'pcolors=' in element:
                    records[pair[0]]=[int(float(x)) for x in pair[1].replace('[','').replace(']','').replace(' ','').split(',')]
                else:
                    records[pair[0]]=int(float(pair[1]))

        self.points=numpy.array(list(zip(records['pathX'],records['pathY'])))
        self.colors=numpy.array(records['pcolors'])
        self.is_closed=records['pclosed']
        if 'pBezier' in records.keys():
            self.is_Bezier=records['pBezier']
        if 'pfillcolor' in records.keys():
            self.fillcolor=records['pfillcolor']
        if 'linewidth' in records.keys():
            self.linewidth=records['linewidth']
        if 'circleradius' in records.keys():
            self.circleradius=records['circleradius']
        if 'sectoropening' in records.keys():
            self.sectoropening=records['sectoropening']

    def is_point_in_path(self,point):
        '''Tests whether point is in path, returns index if true, returns -1 if false'''
        distances=numpy.sqrt(((self.points-point.coords)**2).sum(axis=1))
        if distances.min()<drawing_constants.minclosestdistance:
            return distances.argmin()
        else:
            return -1

    def __str__(self):
        '''Convert path to string so it can be saved in a (perl compliant) text file'''
        fullstring='$pathX='+numpy.array2string(self.points[:,0],separator=',').replace('\n','').replace(' ','')+';'
        fullstring+='$pathY='+numpy.array2string(self.points[:,1],separator=',').replace('\n','').replace(' ','')+';'
        fullstring+='$pcolors='+numpy.array2string(self.colors,separator=',').replace('\n','').replace(' ','')+';'
        fullstring+='$pclosed='+str(int(self.is_closed))+';'
        fullstring+='$pfillcolor='+str(int(self.fillcolor))+';'
        fullstring+='$pBezier='+str(int(self.is_Bezier))+';'
        fullstring+='$linewidth='+str(int(self.linewidth))+';'
        fullstring+='$circleradius='+str(int(self.circleradius))+';'
        fullstring+='$sectoropening='+str(int(self.sectoropening))+';'

        return fullstring

#
# end path class
#


class path_collection(object):

    def __init__(self,filename=None):
        '''path collection initialization'''
        self.paths=[path()]
        self.currentpath=0
        self.currentposition=0
        self.predicted_point=None
        self.adjusted_point=None
        try:
            self.set_defaults_from_adjustments()
        except:
            self.circleradius_default=150
            self.sectoropening_default=30
            self.linewidth_default=32

        if filename is not None:
            self.read_from_v1_file(filename)

    def reset_predicted_point(self):
        '''reset the predicted point'''
        self.predicted_point=None

    def reset_adjusted_point(self):
        '''reset the predicted point'''
        self.adjusted_point=None

    def set_current_to_adjusted_point(self):
        '''set the current point in the current path to its adjusted point'''
        if self.adjusted_point is not None and drawing_status.MoveMode and not drawing_status.SelectPathMode:
#           we are in move mode, but have already selected a point
            self.replace_point_in_current_path(self.adjusted_point)
#           put us back in select mode to select the next point
            if not drawing_status.SelectPathMode:
                drawing_status.toggle_selectmode()
            update_toolbar()

    def set_current_to_predicted_point(self):
        '''set the current point in the current path to its predicted point'''
        if self.predicted_point is not None and drawing_status.MoveMode and not drawing_status.SelectPathMode:
#           we are in move mode, but have already selected a point
            self.replace_point_in_current_path(self.predicted_point)
#           put us back in select mode to select the next point
            if not drawing_status.SelectPathMode:
                drawing_status.toggle_selectmode()
            update_toolbar()

    def mark_all_dirty(self):
        '''mark all paths as dirty'''
        for path in self.paths:
            path.mark_dirty()

    def increase_fill_color_in_current_path(self):
        '''cycle throught fill colors in current path'''
        self.paths[self.currentpath].increase_fill_color()

    def mark_current_path_segment_black(self):
        '''mark segment at position as black'''
        self.paths[self.currentpath].mark_segment_black(self.currentposition)

    def mark_current_path_segment_transparent(self):
        '''mark segment at position as transparent'''
        self.paths[self.currentpath].mark_segment_transparent(self.currentposition)

    def set_current_path_values_from_adjustments(self):
        '''set the current path constants from the adjustments'''
        self.paths[self.currentpath].set_values_from_adjustments()

    def set_current_path_as_Bezier(self):
        '''mark the current path as Bezier'''
        self.paths[self.currentpath].set_as_Bezier()

    def set_current_path_as_Polygon(self):
        '''mark the current path as Polygon (=non Bezier)'''
        self.paths[self.currentpath].set_as_Polygon()

    def set_current_path_open(self):
        '''mark current path as open'''
        self.paths[self.currentpath].set_open()

    def set_current_path_closed(self):
        '''mark current path as open'''
        self.paths[self.currentpath].set_closed()

    def add_point_to_current_path(self,point):
        '''add point at position in current path'''
        self.paths[self.currentpath].add_point(point,self.currentposition)
        self.currentposition+=1

    def delete_point_from_current_path(self):
        '''delete point at position in current path'''
        self.paths[self.currentpath].delete_point(self.currentposition)
        update_toolbar()        

    def replace_point_in_current_path(self,point):
        '''replace point at current position'''
        self.paths[self.currentpath].replace_point(point, self.currentposition)
        self.currentposition+=1        

    def read_from_v1_file(self,filename):
        '''Read collection of paths from a v1 (=perl) file'''
        newpaths=[]
        records={}
        with gzip.open(filename,'r') as f:
            for line in f.readlines():
                line=line.decode()
                if 'pathX' in line:
                    newpaths.append(path(line=line))
                else:
                    line=line.replace('$','').replace('\n','').replace(';','').replace(' ','')
                    pair=line.split('=')
                    records[pair[0]]=pair[1]

#       add an empty path at the end of the newly read paths
        self.paths=newpaths
#       create a new empty path so we can start drawing right away
        self.newpath()

###########################################################
#       not sure if we want to use these
#
#        if 'currentpath' in records.keys():
#            self.currentpath=records['currentpath']
#        if 'currentpos' in records.keys():
#            self.currentposition=records['currentpos']
#
#       end not sure section
###########################################################

        if 'degrees_default' in records.keys():
            self.sectoropening_default=records['degrees_default']
        if 'circleradius_default' in records.keys():
            self.circleradius_default=records['circleradius_default']
        if 'linewidth_default' in records.keys():
            self.linewidth_default=records['linewidth_default']

        try:
            self.set_adjustments_to_defaults()
        except:
            pass

    def range_interval(self):
        '''Compute the range ([[minx,miny],[maxx,maxy]]) of all path coordinates'''
        range_interval=self.paths[0].range_interval()
        for path in self.paths:
            if not path.isempty():
                 newrange=numpy.concatenate((range_interval,path.range_interval()))
                 range_interval[0,:]=newrange.min(axis=0)
                 range_interval[1,:]=newrange.max(axis=0)

        return range_interval

    def pdf_scale(self):
        '''Scale a path so that its points occupy the most of an A4 pdf paper'''
        range_interval=self.range_interval()
        ranges=numpy.diff(range_interval,axis=0).reshape(2,)

        for path in self.paths:

            path.mark_dirty()


            points=path.points
            rotate=False
            if ranges[0]>ranges[1]:
    #           x-range is bigger than y-range, so we swap x and y to get a landscape picture
                rotate=True
                range_interval=range_interval[:,[1,0]]
                points=points[:,[1,0]]
                ranges=ranges[[1,0]]

            if ranges[1]<ranges[0]/595*842:
                pscale=595*8/10
                scale=ranges[0]
            else:
                pscale=842*8/10
                scale=ranges[1]

            center=range_interval.mean(axis=0)



            points[:,0]=297.5+(points[:,0]-center[0])*pscale/scale
            # if we rotate, we have swapped x and y, so we need a - sign on y to complete the rotation
            if rotate:
                points[:,1]=421-(points[:,1]-center[1])*pscale/scale
            else:
                points[:,1]=421+(points[:,1]-center[1])*pscale/scale

            path.points=points

        return pscale/scale




    def set_defaults_from_adjustments(self):
        '''set defaults value for constants from sliders'''
        self.circleradius_default=circleradiusadjustment.get_value()
        self.sectoropening_default=sectoropeningadjustment.get_value()
        self.linewidth_default=linewidthadjustment.get_value()

    def set_adjustments_to_defaults(self):
        '''set defaults value for constants from sliders'''
        circleradiusadjustment.set_value(self.circleradius_default)
        sectoropeningadjustment.set_value(self.sectoropening_default)
        linewidthadjustment.set_value(self.linewidth_default)

    def draw_all(self,context,withpoints=True,linewidth_scale=1):
        '''Draw all paths from the collection'''
#       draw all the paths using the Cairo context
        for pathcount,path in enumerate(self.paths):
            if not path.isempty():
#               but only if the path is not empty
                path.draw(context,currentflag=pathcount==self.currentpath,currentposition=self.currentposition,withpoints=withpoints,linewidth_scale=linewidth_scale)

#       now draw and compute the adjusted and predicted points, as well as the circle/sector where the predicted point lies
        if drawing_status.DrawMode and withpoints and (self.currentposition>-1) and ( (  drawing_status.AddMode or drawing_status.MoveMode ) and not drawing_status.SelectPathMode   ):
            currentpath=self.paths[self.currentpath]
            currentposition=self.currentposition

            if not currentpath.isempty():

                if drawing_status.AddMode:
                    coords=currentpath.points[currentposition-1,:]
                    if (len(currentpath.points)>1):
                        tangent_vector=currentpath.tangents[currentposition-1,:]

                if drawing_status.MoveMode:
                    coords=currentpath.points[currentposition,:]
                    if (len(currentpath.points)>1):
                        tangent_vector=currentpath.tangents[currentposition,:]

                    if currentposition>0:
                        coords_prev_point=currentpath.points[currentposition-1,:]
                    elif (currentposition==0) and currentpath.is_closed:
                        coords_prev_point=currentpath.points[-1,:]
                    elif (currentposition==0) and not currentpath.is_closed and (len(currentpath.points)>1):
                        coords_prev_point=currentpath.points[1,:]

                drawing_constants.set_from_path(currentpath)
                circleradius=drawing_constants.circleradius

                first_angle = None
                last_angle  = None

                self.adjusted_point  = None

                if (len(currentpath.points)==1) and drawing_status.AddMode:
                    # there is only one point in our qpath, so we draw a circle around it (that is, an arc from -Pi to Pi)
                    first_angle = -numpy.pi
                    last_angle  =  numpy.pi



                if (len(currentpath.points)>1):

                    if drawing_status.MoveMode and (currentposition>0 or currentpath.is_closed):

                        tangent_vector_prev_point=currentpath.tangents[currentposition-1,:]

                    if drawing_status.MoveMode and (currentposition==0 and not currentpath.is_closed):

                        tangent_vector_prev_point=-currentpath.tangents[1,:]


                    if drawing_status.MoveMode:
                        # if we are moving mode, we draw a rectangle around the current point. This marks the area over which the "auto-adjust wrt local intensity" (key=a) will apply
                        vector=tangent_vector

                        context.set_source_rgba(1.0,0,0,1)
                        context.set_line_width(1)
                        context.move_to(coords[0]+0.6194*drawing_constants.longirange*vector[0]+drawing_constants.latirange*vector[1],coords[1]+0.6194*drawing_constants.longirange*vector[1]-drawing_constants.latirange*vector[0])
                        context.line_to(coords[0]+0.6194*drawing_constants.longirange*vector[0]-drawing_constants.latirange*vector[1],coords[1]+0.6194*drawing_constants.longirange*vector[1]+drawing_constants.latirange*vector[0])
                        context.line_to(coords[0]-0.6194*drawing_constants.longirange*vector[0]-drawing_constants.latirange*vector[1],coords[1]-0.6194*drawing_constants.longirange*vector[1]+drawing_constants.latirange*vector[0])
                        context.line_to(coords[0]-0.6194*drawing_constants.longirange*vector[0]+drawing_constants.latirange*vector[1],coords[1]-0.6194*drawing_constants.longirange*vector[1]-drawing_constants.latirange*vector[0])
                        context.line_to(coords[0]+0.6194*drawing_constants.longirange*vector[0]+drawing_constants.latirange*vector[1],coords[1]+0.6194*drawing_constants.longirange*vector[1]-drawing_constants.latirange*vector[0])
                        context.stroke()

                        self.adjusted_point=point(coords,do_scaling=False)
                        self.adjusted_point.replace_with_weighted_average(tangent_vector)




                    if drawing_status.AddMode or drawing_status.MoveMode:
#                       draw the sector for point prediction
                        if drawing_status.MoveMode:
#                           if we are in MoveMode, we want to have the sector emanate from the previous point, not the current point
                            coords=coords_prev_point
                            tangent_vector=tangent_vector_prev_point

                        # change the pen color to light gray and small linewidth
                        context.set_source_rgba(0.3,0.3,0.3,1)
                        context.set_line_width(drawing_constants.linewidth/4);

                        # tangent vector at current point
                        vector=tangent_vector

                        # angle of said vector wrt x-axis
                        angle=math.atan2(vector[1],vector[0])
                        deg=drawing_constants.sectoropening/180*numpy.pi

                        first_angle = angle-deg
                        last_angle  = angle+deg


                if first_angle is not None:
#                   there is a sector/circle to be drawn

                    if (last_angle-first_angle<2*numpy.pi):
                        # we do not draw a full circle, so we draw the outer rays of the sector (pie slice)
                        context.move_to(coords[0],coords[1]);
                        context.line_to(coords[0]+circleradius*math.cos(last_angle),coords[1]+circleradius*math.sin(last_angle))
                        context.stroke()
                        context.move_to(coords[0],coords[1])
                        context.line_to(coords[0]+circleradius*math.cos(first_angle),coords[1]+circleradius*math.sin(first_angle))
                        context.stroke()


                    context.set_source_rgba(0.3,0.3,0.3,1)
                    context.set_line_width(drawing_constants.linewidth/4)
                    context.arc (coords[0],coords[1],circleradius,first_angle,last_angle)
                    context.stroke()


                    if self.predicted_point is None:
#                       compute the predicted point (point of max intensity along the circle/sector boundary) 
                        best_weight=0
                        numpoints=int(4*circleradius/drawing_constants.latirange*(last_angle-first_angle))
                        allangles=numpy.linspace(first_angle,last_angle,num=numpoints)
                        for cc,angle in enumerate(allangles):
                            # a point on the circle/sector
                            rX=coords[0]+circleradius*math.cos(angle)
                            rY=coords[1]+circleradius*math.sin(angle)
                            # and its corresponding tangent vector
                            tangent_vector=numpy.array([math.cos(angle),math.sin(angle)])
                            newpoint=point(rX,rY,do_scaling=False)
                            newpoint.replace_with_weighted_average(tangent_vector)
                            if newpoint.weight>best_weight:
                                best_weight=newpoint.weight
                                self.predicted_point=newpoint


                    if self.predicted_point is not None:
#                       mark the predicted point 
                        context.set_source_rgba(0.3,0.3,0.3,0.5)
                        context.arc (self.predicted_point.x,self.predicted_point.y,3*drawing_constants.pointrad,-numpy.pi,numpy.pi)
                        context.fill()
                        context.set_source_rgba(0.3,0.3,0.3,1)
                        context.arc (self.predicted_point.x,self.predicted_point.y,3*drawing_constants.pointrad*2/3,-numpy.pi,numpy.pi)
                        context.fill()
                        context.set_source_rgba(1.0,1.0,1.0,1)
                        context.arc (self.predicted_point.x,self.predicted_point.y,3*drawing_constants.pointrad*1/3,-numpy.pi,numpy.pi)
                        context.fill()

                    if self.adjusted_point is not None:
#                       mark the adjusted point
                        context.set_source_rgba(0.3,0.3,0.3,0.5)
                        context.arc (self.adjusted_point.x,self.adjusted_point.y,3*drawing_constants.pointrad,-numpy.pi,numpy.pi)
                        context.fill()
                        context.set_source_rgba(0.3,0.3,0.3,1)
                        context.arc (self.adjusted_point.x,self.adjusted_point.y,3*drawing_constants.pointrad*2/3,-numpy.pi,numpy.pi)
                        context.fill()
                        context.set_source_rgba(1.0,1.0,1.0,1)
                        context.arc (self.adjusted_point.x,self.adjusted_point.y,3*drawing_constants.pointrad*1/3,-numpy.pi,numpy.pi)
                        context.fill()


        context.show_page()


    def newpath(self):
        '''create a new path using the defaults values'''
        newpath=path(linewidth=self.linewidth_default,circleradius=self.circleradius_default,sectoropening=self.sectoropening_default)
        self.paths.append(newpath)
        self.currentpath=len(self.paths)-1
        self.currentposition=0

    def export(self,filename):
        '''export all path to a file'''
#       first export the raw data to a gz file
        str_representation=str(allpaths)
        with gzip.open(original_image.points_file, 'w') as f:
            f.write(str_representation.encode())

#       A4 paper has standard size 595x842 in whatever units
        pdfsurface = cairo.PDFSurface(original_image.pdf_file, 595, 842)

#       fill the page as white
        context = cairo.Context( pdfsurface )
        context.set_source_rgba(1.0, 1.0, 1.0, 1)
        context.rectangle(0,0,595,842);
        context.fill()

#       here we use the fact that we just saved the path collection to a file
#       so we can read it into a _new_ collection
        pdf_paths=path_collection()
        pdf_paths.read_from_v1_file(original_image.points_file)
#       in the new collection, we can scale the points to fit on A4 paper
        scale=pdf_paths.pdf_scale()
#       draw all the points to the PDF
        pdf_paths.draw_all(context,withpoints=False,linewidth_scale=scale)
#       close the surface
        pdfsurface.finish()


        # open pdf file, works at least in linux, if okular and which are installed
        if os.name=='nt':
            os.system(original_image.pdf_file)
        else:
            try:
                os.system('okular {}'.format(original_image.pdf_file))
            except:
                print('I cannot invoke okular? Please fix this.')


    def get_current_path_and_position_values(self,mypoint):
        '''Find which point in which path is the one we clicked on'''
        found=False
        self.current_point=None
        for count,path in enumerate(self.paths):
            if not path.isempty():
                pointindex=path.is_point_in_path(mypoint)
                if pointindex>=0:
                    found=True
#                   we found the point
                    if drawing_status.SelectPathMode:
                        self.currentpath=count
                        self.currentposition=pointindex
                    coords=self.paths[count].points[pointindex]
                    self.current_point=point(coords,do_scaling=False)

        if found:               
            # if we are in addmode, the index of the next point we drop is one more than the current one            
            if drawing_status.AddMode and drawing_status.SelectPathMode:
                self.currentposition+=1

        return found


    def __str__(self):
        '''Convert path collection to string so it can be saved in a (perl compliant) text file'''
        fullstring='\n'.join([str(path) for path in self.paths if not path.isempty()])+'\n'
        fullstring+='$currentpath='+str(self.currentpath)+';\n'
        fullstring+='$currentpos='+str(self.currentposition)+';\n'
        fullstring+='$circleradius_default='+str(self.circleradius_default)+';\n'
        fullstring+='$degrees_default='+str(self.sectoropening_default)+';\n'
        fullstring+='$linewidth_default='+str(self.linewidth_default)+';\n'
        return fullstring

#
# end path_collection class
#


#%%

def longicut(x,myrange):
    '''exponential weight to cut averages outside myarange'''
    y=numpy.exp(-x*x*6/myrange/myrange)
    return y

def laticut(x,myrange):
    '''heaviside weight to cut averages outside myarange'''
    return abs(x)<myrange

#%%

def update_statusbar():
    '''update the status bar with the appropriate message'''

    statusbar.pop(0); # clear any previous message, underflow is allowed (wtf does this means)
    if drawing_status.DrawMode:
        if drawing_status.MoveMode and drawing_status.SelectPathMode:
            statusbar.push (0, "   Choose point to be moved")

        if drawing_status.MoveMode and not drawing_status.SelectPathMode:
            statusbar.push (0, "   Click where point is to be moved")

        if drawing_status.DeleteMode:
            statusbar.push (0, "   Choose point to be deleted")

        if drawing_status.AddMode and drawing_status.SelectPathMode:
            statusbar.push (0, "   Choose point after which new point(s) will be added")

        if drawing_status.AddMode and not drawing_status.SelectPathMode:
            statusbar.push (0, "   Click on location of point to be added")
    else:
        if drawing_status.BlackMode:
            statusbar.push (0, "   Choose point at start of segment to be marked as black")
        else:
            statusbar.push (0, "   Choose point at start of segment to be marked as white")




def update_toolbar():
    '''Update the toolbar to reflect the current status'''

    if drawing_status.DrawMode:
#       We are in drawing mode, so we show the "selected" icon and hide the "unselected" one, we also show the open and closed path icons, as well as all separators
        builder.get_object('drawmode').hide()
        builder.get_object('drawmodesel').show()
        builder.get_object('openpath').show()
        builder.get_object('closedpath').show()
        builder.get_object('toolseparator3').show()
        builder.get_object('toolseparator4').show()
        if drawing_status.AddMode:
#           show the "selected" icon, hide the unselected
            builder.get_object('addmodesel').show()
            builder.get_object('addmode').hide()
        else:
#           or vice-versa depending on status
            builder.get_object('addmodesel').hide()
            builder.get_object('addmode').show()
        if drawing_status.MoveMode:
#           show the "selected" icon, hide the unselected
            builder.get_object('movemodesel').show()
            builder.get_object('movemode').hide()
        else:
#           or vice-versa depending on status
            builder.get_object('movemodesel').hide()
            builder.get_object('movemode').show()
        if drawing_status.DeleteMode:
#           show the "selected" icon, hide the unselected
            builder.get_object('deletemodesel').show()
            builder.get_object('deletemode').hide()
        else:
#           or vice-versa depending on status
            builder.get_object('deletemodesel').hide()
            builder.get_object('deletemode').show()
        if drawing_status.SelectPathMode:
#           show the "selected" icon, hide the unselected
            builder.get_object('selectmodesel').show()
            builder.get_object('selectmode').hide()
        else:
#           or vice-versa depending on status
            builder.get_object('selectmodesel').hide()
            builder.get_object('selectmode').show()
#       hide the UI elements for the color mode as they are useless in this mode
        builder.get_object('whitemodesel').hide()
        builder.get_object('whitemode').hide()
        builder.get_object('blackmodesel').hide()
        builder.get_object('blackmode').hide()
    else:
#       show the drawmode icon so it can be clicked on, hide the "selected" version
        builder.get_object('drawmode').show()
        builder.get_object('drawmodesel').hide()

    if drawing_status.ColorMode:
#       We are in drawing mode, so we show the "selected" icon and hide the "unselected" one
        builder.get_object('colormode').hide()
        builder.get_object('colormodesel').show()

        if drawing_status.BlackMode:
#           show the "selected" icon, hide the unselected
            builder.get_object('blackmodesel').show()
            builder.get_object('blackmode').hide()
        else:
#           or vice-versa depending on status
            builder.get_object('blackmodesel').hide()
            builder.get_object('blackmode').show()
        if drawing_status.WhiteMode:
#           show the "selected" icon, hide the unselected
            builder.get_object('whitemodesel').show()
            builder.get_object('whitemode').hide()
        else:
#           or vice-versa depending on status
            builder.get_object('whitemodesel').hide()
            builder.get_object('whitemode').show()

#       hide the UI elements for the draw mode as they are useless in this mode
        builder.get_object('toolseparator3').hide()
        builder.get_object('toolseparator4').hide()
        builder.get_object('openpath').hide()
        builder.get_object('closedpath').hide()
        builder.get_object('selectmodesel').hide()
        builder.get_object('selectmode').hide()
        builder.get_object('addmodesel').hide()
        builder.get_object('addmode').hide()
        builder.get_object('addmodesel').hide()
        builder.get_object('addmode').hide()
        builder.get_object('movemodesel').hide()
        builder.get_object('movemode').hide()
        builder.get_object('deletemodesel').hide()
        builder.get_object('deletemode').hide()

    else:
#       show the colormode icon so it can be clicked on, hide the "selected" version
        builder.get_object('colormode').show()
        builder.get_object('colormodesel').hide()

#   update the statusbar as well
    update_statusbar()

class image(object):
    '''A class to hold details in memory about the original png image'''
    def __init__(self,image_file='image.png'):
        '''initialize object'''
        self.image_file=image_file
        self.open_file(image_file)

    def open_file(self,image_file):
        '''open the png file'''
        self.set_pdf_file(image_file.replace('.png','.pdf'))
        if os.path.isfile(image_file):
#           create surface from image file
            self.surface=cairo.ImageSurface.create_from_png(image_file)
        else:
#           create empty (white) surface
            self.surface=cairo.ImageSurface(cairo.FORMAT_ARGB32, 2350, 2350)
            cr=cairo.Context(self.surface)
            cr.set_source_rgb(1.0,1.0,1.0)
            cr.paint()
            self.surface.show_page()

#       get the rgba and intensity matrix, set the width, height, etc
        self.compute_intensity()
#       read the points from previous runs, if they exist
        self.points_file=image_file+'_points_v1.gz'
        if os.path.isfile(self.points_file):
            allpaths.read_from_v1_file(self.points_file)


    def set_pdf_file(self,filename):
        '''Set the pdf filename'''
        self.pdf_file=filename

    def compute_intensity(self):
        '''get the rgba and intensity matrix, set the width, height, etc'''
#       get the pixels (a "memoryview")
        pixels=self.surface.get_data()
#       keep track of the width and height for later use
        self.width=self.surface.get_width()
        self.height=self.surface.get_height()
#       number of bytes per pixel
        self.bytes_per_pixel=int(self.surface.get_stride()/self.width)
#       transform the memoryview into a (big) 1D numpy array
        self.rgba_array = numpy.frombuffer(pixels, dtype=numpy.uint8)
#       reshape into a (HxWxBPP) matrix, note the height comes as first axis and width as second
        self.rgba_array.shape = (self.height,self.width,self.bytes_per_pixel)
#       transpose the first two dimensions
        self.rgba_array=self.rgba_array.transpose((1,0,2))
#       compute the intensity (white has lowest intensity, black has highest)
        self.intensity=(255-self.rgba_array[:,:,0:2]).sum(axis=2)
#       matrices of pixel coordinates
        grid=numpy.meshgrid(range(self.width),range(self.height),indexing='ij')
        self.i=grid[0]
        self.j=grid[1]

#
# end image class
#


if True:




#   build the UI from the design file
    builder = Gtk.Builder()
#    builder.add_from_file("scribble3.glade")
    builder.add_from_string(glade_string)
#   connect the signals from the Handler class
    builder.connect_signals(Handler())

#   get the main UI elements
    window = builder.get_object("window1")
    drawingarea=builder.get_object('drawingarea')
    scrolledwindow=builder.get_object('scrolledwindow')
    progressbar = builder.get_object('progressbar')
    statusbar = builder.get_object('statusbar');
    toolbar = builder.get_object('toolbar')
#   get the UI elements that can be toggled
    AutoScroll = builder.get_object("AutoScrollMenu")
    UseClosestPoint = builder.get_object("UseClosestPointMenu")
    AutoAdjustPoints = builder.get_object("AutoAdjustPointsMenu")
    circleradiusadjustment=builder.get_object('circleradiusadjustment')
    sectoropeningadjustment=builder.get_object('sectoropeningadjustment')
    linewidthadjustment=builder.get_object('linewidthadjustment')
#   auxiliary windows
    scribblesettingswindow=builder.get_object('scribblesettingswindow')
#   drawing area subscribes to all events
    drawingarea.set_events (Gdk.EventMask.ALL_EVENTS_MASK)

#   size the main window
    window.set_size_request(800,600)
#   add our own icons, connect the toolbar callbacks, add the toolbar tooltips
    setup_UI()
    window.set_title ("Bezier Scribble")

#   initialize the UI status
    drawing_status=status()
#   initialize all paths
    allpaths=path_collection()

#   open the png file, set the associated parameters
    image_file='image.png'
    original_image=image(image_file)
#   initialize the drawing constants
    drawing_constants=constants()

#   setup the drawing area
    drawing_status.set_scale(2350/original_image.width)
    drawingarea.set_size_request (original_image.width*drawing_status.scale,original_image.height*drawing_status.scale)
#   listen to events again ? 
    drawingarea.set_events(drawingarea.get_events()| Gdk.EventMask.BUTTON_PRESS_MASK) #| Gdk.EventMask.LEAVE_NOTIFY_MASK| Gdk.EventMask.POINTER_MOTION_MASK| Gdk.EventMask.POINTER_MOTION_HINT_MASK
#%%

#%%



#   show all elements
    window.show_all()
#   move the window out of the view (TODO: remove)
#    if os.name=='nt':
#        window.move(10000,2000)


#   but hide the progressbar
    progressbar.hide()
#    builder.get_object('UselessHelpButton').hide()
#   update the toolbar so it reflects the current status
    update_toolbar()



#   main loop
    Gtk.main()
