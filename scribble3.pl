#!/usr/bin/perl -w

#----------------------------------------------------------------
#
#  use section
#
use warnings;
use strict;
use Cairo;
use Glib qw/TRUE FALSE/;
use Gtk3;
use Glib;
#use Gtk3::Gdk;
use Image::Size;
use List::Util qw( max min );
use List::MoreUtils qw( minmax );
use Config;
use Data::Dumper;
use Compress::Zlib;
use MIME::Base64::Perl;
use Text::CSV_XS qw( csv );
#
# end use section
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#
#             initialization
#
#
if($Config{osname} eq 'linux'){
  # linux specific initialization
  
}else{
  # windows specific initialization 
  
  # use native window decorations
  $ENV{'GTK_CSD'}=0;
  $ENV{'GTK_THEME'}='Breeze';
}



my $millimeter_width_for_export=0.9;   # linewidth in millimeters in pdf output
my $mindistance=15;                    # will not record point that are closer than this to each other (in current path)

my $maxdist = 3;                # if distance between mouse coordinates and current pointer position
                                # is bigger than this, it means we are not reading the correct pointer
my $pi=3.1415926;               # lol
my $debug=0;                    # will output some things if set to 1

my $scale=1;                    # scaling of the image for zooming
my $millimeter_width=0.9;       # linewidth in millimeters (for a 2350 pixel wide image)

my @lastpoint=();               # we will not record a point that is too close to previous
$lastpoint[0]=-1000;            # recorded point, in space or time.
$lastpoint[1]=-1000;            # we set these to dummy values to compare later
my $lasttime=0;

my $predictX= undef;            # coordinates predicted for next point
my $predictY= undef;            # uses light intensity matrix derived from image

my $circleradius;               # a slider (range) to set the radius between points
my $circleradius_default=150;   # and its default value
my $degrees;                    # slider for opening of sector where to look for new points
my $degrees_default=30;         # and its default value
my $linewidthslider;            # a slider for the linewidth
my $linewidth_default=32;       # and its default value

my $pngname="big.png";          # this will be (optionally) set by an open dialog later...
my $pdfname=$pngname;           # name of the pdf file for output
$pdfname=~ s/\.[\w\W]+/\.pdf/g;

my ($width,$height,$stride,$cformat); # info about our background image (surface)

my $window = undef;             # our main window
my $table = undef;              # our main window's table
my $drawing_area = undef;       # and this the drawing area
my $ScrolledWindow = undef;     # container for drawing area

my $oldstyle=0;                 # switching between modes is implemented by the buttons below.
                                # unless $oldstyle is set to 1, the buttons are hidden

my $btn_colormode = undef;     # There are two main modes: coloring
my $btn_drawmode  = undef;     # and drawing. In drawing mode,
my $btn_addmode = undef;       # we have three modes: adding points
my $btn_delmode = undef;       # deleting points
my $btn_movmode = undef;       # and moving points
my $btn_selectpath = undef;    # some mode require a path/point to be selected all the time or not
my $btn_blackmode = undef;     # segments are black by default
my $btn_whitemode = undef;     # but some may be white

my $btn_anyposition = undef;    # points can be dropped at any position
my $btn_closestposition = undef;# or we can force them to coincide with the closest existing one
my $btn_quit = undef;           # a quit button (deprecated, moved to menu/toolbar)
my $btn_config = undef;         # a config button (deprecated, moved to menubar)
my $btn_open = undef;           # an open button (deprecated, moved to menu/toolbar)
my $btn_save = undef;           # a save button (deprecated, moved to menu/toolbar)
my $btn_save_as = undef;        # a save as button (deprecated, moved to menu/toolbar)
my $btn_AutoScroll = undef;     # flag to center the scrolling on last mouse click or not

my $buttonbox = undef;                 # this will hold the optional right panel with buttons
my $menubar = undef;                   # the menubar
my $statusbar = undef;                 # the statusbar
my $toolbar = undef;                   # the toolbar
my $ui = undef;                        # the UI manager
my $ui_info_toolbar_drawmode = undef;  # we have two different toolbars. One for drawing mode
my $ui_info_toolbar_colormode = undef; # and one for coloring mode. Creating the toolbar and menubar will
my $toolbar_magic = undef;             # set this variable and the next one. We can then use it to replace it with
my $menubar_magic = undef;             # the other tool/menubar when we change from one mode to the other

my $modeframe = undef;       # four frames to hold some
my $colorframe = undef;      # buttons and make the "oldstyle" interface
my $positionframe = undef;   # nicer
my $newpathframe = undef;    #

my $withpoints=1;            # flag to display points or not on paths (autoset to 0 for pdf output)

my $framewidth=150;          # some settings to force appearance of "oldstyle"
my $buttonwidth=80;          # right hand side panel
my $buttonheight=28;         # this is useless, unless $oldstyle=1 (for debugging)

my @allX=();                 # will contain all X coordinates of our paths
my @allY=();                 # and Y coordinates
my @closed=();               # will contain flags to denote open or closed path
my @colors=();               # will contain black/white flag or segments in our paths
my $currentpath=0;           # index of path being currently modified
my $currentpos=0;            # index (position) of point being currently modified

my @intensity=();            # intensity matrix from png file

$closed[0]=0;          # by default paths are open
push(@allX,[]);        # start populating the paths
push(@allY,[]);        # and colors with
push(@colors,[]);      # anonymous arrays

my $keepsurface;       # the "surface" that will hold the data from the png file
                       # we keep it in memory, so we don't need to reread the file later on

# read the file once, get the details of the Cairo surface for later redrawing
if(-e "$pngname"){
  # our original surface from the png file
  $keepsurface = Cairo::ImageSurface->create_from_png($pngname);
}else{
  # create an empty surface in case the png file does not exist
  $width=2350;
  $height=2350;
  $keepsurface = Cairo::ImageSurface->create('rgb24', $width, $height);
}

# now get the surface details for repainting later on
$width=$keepsurface->get_width;
$height=$keepsurface->get_height;
$stride=$keepsurface->get_stride;
$cformat=$keepsurface->get_format;
$scale=2350/$width;

# derived constants (point width, line width and point radius
my $pwidth=$millimeter_width*$width/210;
my $linewidth=$millimeter_width*$width/210;
my $pointrad=$linewidth/4;

my $longirange=$linewidth;    # in auto-adjust: width of weight support in direction tangent to path (Gaussian weight<0.1 outside range)
my $latirange=$linewidth;     # in auto-adjust: width of weight support in direction perpend to path (weight=0 outside range)

# in "closest" mode, will replace current point by any (other) existing point whose distance is less than this:
my $minclosestdistance=$linewidth;

# import paths corresponding to current image from previous run if they exist
myimport();
#
#               end initialisation
#
#----------------------------------------------------------------




#--------------------------------------------------------------------------------------------------------
#
#                User Interface Initialization
#

# fixed menu entries
my @entries = (
  # name,                 stock id,  label
  [ "FileMenu",           undef,     "_File"        ],
  [ "SettingsMenu",       undef,     "Settin_gs"    ],
  [ "PointPositionMenu",  undef,     "_Point Position"    ],
  # name,             stock id,                    label,            accelerator  ,    tooltip                                        callback
  [ "Open"          , 'gtk-open'                 , "_Open Image"   , "<control>O" , "Open an image file"                            , \&show_chooser_png ],
  [ "Save"          , 'gtk-save'                 , "_Export"       , "<control>S" , "Export paths"                                  , \&export ],
  [ "SaveAs"        , 'gtk-save-as'              , "Export _As"    ,  undef       , "Export paths to a file"                        , \&show_chooser_pdf ],
  [ "Quit"          , 'gtk-quit'                 , "_Quit"         , "<control>Q" , "Quit"                                          , \&quitapp ],
  #[ "Input"         , undef                      , "_Input Dialog" ,  undef       , "Input Dialog"                                  , \&create_input_dialog ],
  [ "Config"        , 'gtk-preferences'          , "_Config"       ,  undef       , "Config"                                        , \&configure ],
  [ "OpenNewPath"   , "scribble-open-path"       , "ope_n"         ,  undef       , "Start new path, marking current one as open"   , \&opennewpath ],
  [ "ClosedNewPath" , "scribble-closed-path"     , "_closed"       ,  undef       , "Start new path, marking current one as closed" , \&closenewpath ],

  [ "AddMode"       , "scribble-add-mode"        , "_Add"          ,  undef       , "Add point to path"                             , \&setaddmode ],
  [ "DelMode"       , "scribble-del-mode"        , "_Delete"       ,  undef       , "Delete point from path"                        , \&setdelmode ],
  [ "MoveMode"      , "scribble-move-mode"       , "_Move"         ,  undef       , "Move point in path"                            , \&setmovemode ],

  [ "AddModeSel"    , "scribble-add-mode-sel"    , "_Add"          ,  undef       , "Add point to path"                             , \&setaddmode ],
  [ "DelModeSel"    , "scribble-del-mode-sel"    , "_Delete"       ,  undef       , "Delete point from path"                        , \&setdelmode ],
  [ "MoveModeSel"   , "scribble-move-mode-sel"   , "_Move"         ,  undef       , "Move point in path"                            , \&setmovemode ],

  [ "BlackMode"     , "scribble-black-mode"      , "_Black"        ,  undef       , "Mark next segment as black"                    , \&setblackmode ],
  [ "WhiteMode"     , "scribble-white-mode"      , "_White"        ,  undef       , "Mark next segment as white"                    , \&setwhitemode ],

  [ "BlackModeSel"  , "scribble-black-mode-sel"  , "_Black"        ,  undef       , "Mark next segment as black"                    , \&setblackmode ],
  [ "WhiteModeSel"  , "scribble-white-mode-sel"  , "_White"        ,  undef       , "Mark next segment as white"                    , \&setwhitemode ],

  [ "SelectPath"    , "scribble-select-path"     , "Select _Path"  , "<alt>P"     , "SelectPath Toggle"                             , \&toggleselectpath],
  [ "SelectPathSel" , "scribble-select-path-sel" , "Select _Path"  , "<alt>P"     , "SelectPath Toggle"                             , \&toggleselectpath],

  [ "ColorMode"     , "scribble-color-mode"      , "Color m_ode"   ,  undef       , "Color Mode Toggle"                             , \&togglecolormode ],
  [ "DrawMode"      , "scribble-draw-mode"       , "Draw m_ode"    ,  undef       , "Draw Mode Toggle"                              , \&toggledrawmode ],

  [ "ColorModeSel"  , "scribble-color-mode-sel"  , "Color m_ode"   ,  undef       , "Color Mode Toggle"                             , \&togglecolormode ],
  [ "DrawModeSel"   , "scribble-draw-mode-sel"   , "Draw m_ode"    ,  undef       , "Draw Mode Toggle"                              , \&toggledrawmode ],

  [ "ZoomIn"        , 'gtk-zoom-in'              , "Zoom _In"      , "plus"       , "Zoom In"                                       , \&zoomin ],
  [ "ZoomOut"       , 'gtk-zoom-out'             , "Zoom _Out"     , "minus"      , "Zoom Out"                                      , \&zoomout ],

);

# menu entries that can be toggled
my @toggle_entries = (
#    name,             stock id     , label         ,  accelerator , tooltip     ,   callback,       is_active
  [ "AutoScrollTrue" , undef        , "Auto_Scroll" ,  "<alt>s"    , "AutoScroll",  \&autoscrolltoggle, TRUE ],
  [ "AutoScrollFalse", undef        , "Auto_Scroll" ,  "<alt>s"    , "AutoScroll",  \&autoscrolltoggle, FALSE ],
);

use constant CLOSEST   => 1;
use constant ANY       => 0;
my @pointposition_entries = (
  # name,    stock id, label,    accelerator ,  tooltip, value
  [ "Closest", undef, "_Closest", undef      , "Drop new point at any existing point closer than linewidth if one exists", CLOSEST   ],
  [ "Any"    , undef, "_Any"    , undef      , "Drop points at any position", ANY ],
);

# menubar
my $ui_info_menubar = "<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='Open'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='SettingsMenu'>
      <menu action='PointPositionMenu'>
   <menuitem action='Closest'/>
   <menuitem action='Any'/>
      </menu>
      <menuitem action='AutoScroll'/>
      <menuitem action='Config'/>
      <menuitem action='ZoomIn'/>
      <menuitem action='ZoomOut'/>
    </menu>
  </menubar>
</ui>";

#      <menuitem action='Input'/>  above PointPositionMenu

# bare toolbar in drawmode
$ui_info_toolbar_drawmode = "<ui>
  <toolbar  name='ToolBar'>
    <toolitem action='Open'/>
    <toolitem action='Save'/>
    <toolitem action='SaveAs'/>
    <toolitem action='Quit'/>
    <separator action='Sep1'/>
    <toolitem action='DrawMode'/>
    <toolitem action='ColorMode'/>
    <separator action='Sep2'/>
    <toolitem action='OpenNewPath'/>
    <toolitem action='ClosedNewPath'/>
    <separator action='Sep3'/>
    <toolitem action='AddMode'/>
    <toolitem action='MoveMode'/>
    <toolitem action='DelMode'/>
    <separator action='Sep4'/>
    <toolitem action='SelectPath'/>
    <separator action='Sep5'/>
    <toolitem action='ZoomIn'/>
    <toolitem action='ZoomOut'/>
  </toolbar>
</ui>";

# bare toolbar in colormode
$ui_info_toolbar_colormode = "<ui>
  <toolbar  name='ToolBar'>
    <toolitem action='Open'/>
    <toolitem action='Save'/>
    <toolitem action='SaveAs'/>
    <toolitem action='Quit'/>
    <separator action='Sep1'/>
    <toolitem action='DrawMode'/>
    <toolitem action='ColorMode'/>
    <separator action='Sep2'/>
    <toolitem action='BlackMode'/>
    <toolitem action='WhiteMode'/>
    <separator action='Sep3'/>
    <toolitem action='ZoomIn'/>
    <toolitem action='ZoomOut'/>
  </toolbar>
</ui>";
#
#        end User Interface Initialization
#
#--------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------
#
#
#       main Gtk3 stuff
#
#
{
Gtk3->init;

# setup the sliders for the circle/sector radius, sector opening and linewidth
sliders_setup();

# set our icons into stock so they can be called as stock elements and/or themed later
register_stock_icons ();

#        main window
$window = Gtk3::Window->new ('toplevel');
if($Config{osname} eq 'linux'){
  $window->set_size_request(600,550);
}else{
  $window->set_size_request(800,550);
}
$window->set_title ("scribble");
$window->signal_connect ("destroy", sub { Gtk3->main_quit });
$window->signal_connect('key-press-event' => \&proc_key);

# main window is split in a 1x4 (vertical) table (menubar, toolbar, drawing area, statusbar)
$table = Gtk3::Table->new (1, 4, FALSE);
$window->add ($table);

# Create the menubar
my $actions = Gtk3::ActionGroup->new ("Actions");
$actions->add_actions (\@entries, undef);
$actions->add_toggle_actions (\@toggle_entries, undef);
$actions->add_radio_actions (\@pointposition_entries, CLOSEST ,\&togglepointposition);

# and the UIManager
$ui = Gtk3::UIManager->new;
$ui->insert_action_group ($actions, 0);
$window->add_accel_group ($ui->get_accel_group);

# get default toolbar and menubar
my $ui_menubar=$ui_info_menubar;
my $ui_info_toolbar=$ui_info_toolbar_drawmode;
# adjust them to current state
$ui_menubar=~ s/AutoScroll/AutoScrollTrue/;
$ui_info_toolbar=~ s/AddMode/AddModeSel/;
$ui_info_toolbar=~ s/DrawMode/DrawModeSel/;
# then add them to the UI
$toolbar_magic=$ui->add_ui_from_string ($ui_info_toolbar);
$menubar_magic=$ui->add_ui_from_string ($ui_menubar);
# get the menubar and toolbar so we can add them to the table
$menubar=$ui->get_widget ("/MenuBar");
$toolbar=$ui->get_widget ("/ToolBar");

# Create main drawing area
my $maindrawingarea=createmaindrawingarea();

# Create statusbar
$statusbar = Gtk3::Statusbar->new;
$statusbar->set_size_request(-1,24);
update_statusbar($statusbar);

# attach all ui elements to table
$table->attach ($menubar         ,0,1,0,1,[qw/expand fill/],[],0,0);
$table->attach ($toolbar         ,0,1,1,2,[qw/expand fill/],[],0,0);
$table->attach ($maindrawingarea ,0,1,2,3,[qw/expand fill/],[qw/expand fill/],0,0);
$table->attach ($statusbar       ,0,1,3,4,[qw/expand fill/],[],0,0);

# make sure the two changing UI elements are up to date
update_toolbar();
update_statusbar();

# stupid hack: since most elements are to be shown, show all, then hide the
# one we do not need at the beginning.
$window->show_all;

#           Finalization
$btn_whitemode->hide;
$btn_colormode->hide;
$btn_anyposition->hide;
$colorframe->hide;
if($oldstyle==0){          # hide a few buttons to unclutter the app
  $btn_config->hide;       # unless $oldstyle==1
  $btn_save->hide;
  $newpathframe->hide;
  $btn_closestposition->hide;
  $btn_AutoScroll->hide;
  $positionframe->hide;
  $modeframe->hide;
  $colorframe->hide;
  $btn_selectpath->hide;
  $btn_drawmode->hide;
  $btn_colormode->hide;
  $buttonbox->hide;
}

# main loop
Gtk3->main;

}
#
#
#
#           end main Gtk3 stuff
#
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#
#         exit cleanly
#
#
sub quitapp {
  $window->destroy;
}
#
#
#         end quitapp sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#
#         setup the range/sliders/adjustment for the 
#         circle/sector radius, sector opening and linewidth
#
#
sub sliders_setup {

# syntax for Gtk3::Adjustment is
# value, lower, upper, step_increment, page_increment, page_size
# Note that the page_size value only makes a difference for
# scrollbar widgets, and the highest value you'll get is actually
# (upper - page_size).

  $circleradius = Gtk3::Adjustment->new($circleradius_default, $mindistance, 301.0, 1.0, 1.0, 1.0);
  $circleradius->signal_connect(value_changed => \&queue_drawing);
  $degrees = Gtk3::Adjustment->new($degrees_default, 0, 91.0, 1.0, 1.0, 1.0);
  $degrees->signal_connect(value_changed => \&queue_drawing);
  $linewidthslider = Gtk3::Adjustment->new($linewidth_default,0.0, 100.0, 1.0, 1.0, 1.0);
  $linewidthslider->signal_connect(value_changed => \&set_linewidth_and_related);

  # since the linewidth default might have changed, reset the linewidth and derived params
  set_linewidth_and_related();

}
#
#
#         end sliders_setup sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#
#         set sliders for circle/sector radius, sector opening 
#         and linewidth to default values
#         
#
#
sub sliders_set_to_defaults {
  $circleradius->set_value(150);
  $degrees->set_value(30);
  $linewidthslider->set_value(32);

  # since the linewidth default might have changed, reset the linewidth and derived params
  set_linewidth_and_related();
}
#
#
#         end sliders_setup sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#
#     reset last point values so we can ignore them later
#     mainly used when we click on a UI element, so we can
#     later click on the last recorded point to modify it
#     otherwise our click would be rejected as "too close"
#     to last recorded point
#
#
sub reset_lastpoint{
  $lastpoint[0]=-1000;
  $lastpoint[1]=-1000;
  $lasttime=0;
}
#
#
#     end reset_lastpoint sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     in case we change the autoscroll mode automatically,
#     we need to update the menubar to reflect that change
#
sub toggleautoscrollbtn {
  update_menubar();
}
#
#     end toggleautoscrollbtn sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     when we enter/leave colormode, the UI changes.
#     In colormode, we always select point, and need
#     to change path colors.
#     If we enter drawmode, we need to select a point
#     (or start a new path).
#     Both modes, being exclusive, need to hide the other's
#     UI element
#
sub togglecolormodebtn {
  if($btn_colormode->get_active){
    $btn_addmode->set_active(TRUE);
    $btn_selectpath->set_active(TRUE);
    $btn_selectpath->hide;
    $btn_drawmode->set_active(FALSE);
    if($oldstyle==1){
      $colorframe->show;
    }
  }else{
    if($oldstyle==1){
      $btn_selectpath->show;
      $btn_drawmode->show;
    }
    $colorframe->hide;
    $btn_colormode->hide;
    $btn_drawmode->set_active(TRUE);
    $btn_addmode->set_active(TRUE);
  }
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#----------------------------------------------------------------
sub toggledrawmodebtn{
  if($btn_drawmode->get_active){
    $btn_colormode->set_active(FALSE);
    $btn_selectpath->set_active(TRUE);
    if($oldstyle==1){
      $newpathframe->show;
      $positionframe->show;
      $modeframe->show;
    }
  }else{
    $modeframe->hide;
    $positionframe->hide;
    $newpathframe->hide;
    $btn_drawmode->hide;
    if($oldstyle==1){
      $btn_colormode->show;
    }
    $btn_colormode->set_active(TRUE);
  }
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#
#     end toggledrawmodebtn and togglecolormodebtn
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     the logic was done in the two sub above, here, we only
#     toggle the state (used when clicking on toolbar, say)
#
sub toggledrawmode{
  if($btn_drawmode->get_active){
    $btn_drawmode->set_active(FALSE);
  }else{
    $btn_drawmode->set_active(TRUE);
  }
  # if we click on a UI element, then we can forget about the
  # coordinates of the last point entered
  reset_lastpoint();
}
#----------------------------------------------------------------
sub togglecolormode{
  if($btn_colormode->get_active){
    $btn_colormode->set_active(FALSE);
  }else{
    $btn_colormode->set_active(TRUE);
  }
  # if we click on a UI element, then we can forget about the
  # coordinates of the last point entered
  reset_lastpoint();
}
#
#     end toggledrawmode and togglecolormode
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     Change selectpath mode when toolbar element is clicked
#
sub toggleselectpath{
  if($btn_selectpath->get_active){
    $btn_selectpath->set_active(FALSE);
  }else{
    $btn_selectpath->set_active(TRUE);
  }
  # if we click on a UI element, then we can forget about the
  # coordinates of the last point entered
  reset_lastpoint();
}
#
#      end toggleselectpath sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     Update all UI elements to reflect current selectpath
#     state. This is used by the (usually hidden) button.
#
sub toggleselectpathbtn{
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#
#     end toggleselectpathbtn sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     Toggle toolbar black/white buttons
#     As they are exclusive, they hide each other
#
sub toggleblackmodebtn{
  if($btn_blackmode->get_active){
    $btn_whitemode->set_active(FALSE);
  }else{
    $btn_blackmode->hide;
    if($oldstyle==1){
      $btn_whitemode->show;
    }
    $btn_whitemode->set_active(TRUE);
  }
  reset_lastpoint();
  update_toolbar();
  update_statusbar();
}
#----------------------------------------------------------------
sub togglewhitemodebtn {
  if($btn_whitemode->get_active){
    $btn_blackmode->set_active(FALSE);
  }else{
    if($oldstyle==1){
      $btn_blackmode->show;
    }
    $btn_blackmode->set_active(TRUE);
    $btn_whitemode->hide;
  }
  reset_lastpoint();
  update_toolbar();
  update_statusbar();
}
#
#     end toggleblackmode and togglewhitemode sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     Set black or white mode from toolbar. Logic is done by
#     two above subs.
#
sub setblackmode{
  $btn_blackmode->set_active(TRUE);
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#----------------------------------------------------------------
sub setwhitemode{
  $btn_whitemode->set_active(TRUE);
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#
#     end setblack/whitemode subs
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     next three subs set add/delete/move modes from toolbar
#     changing to addmode forces selectpath mode on.
#
sub setaddmode{
  $btn_addmode->set_active(TRUE);
  $btn_selectpath->set_active(TRUE);
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#----------------------------------------------------------------
sub setdelmode{
  $btn_delmode->set_active(TRUE);
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#----------------------------------------------------------------
sub setmovemode{
  $btn_movmode->set_active(TRUE);
  reset_lastpoint();
  update_statusbar();
  update_toolbar();
}
#
#     end setadd/del/movmode subs
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     the three modes are mutually exclusive, so setting one
#     unsets the others
#
sub addmodebtn {
  if($btn_addmode->get_active){
    $btn_delmode->set_active(FALSE);
    $btn_movmode->set_active(FALSE);
    $btn_selectpath->set_active(TRUE);
  }
}
#----------------------------------------------------------------
sub movmodebtn {
  if($btn_movmode->get_active){
    $btn_delmode->set_active(FALSE);
    $btn_addmode->set_active(FALSE);
    $btn_selectpath->set_active(TRUE);
  }
}
#----------------------------------------------------------------
sub delmodebtn {
  if($btn_delmode->get_active){
    $btn_addmode->set_active(FALSE);
    $btn_movmode->set_active(FALSE);
    $btn_selectpath->set_active(TRUE);
  }
}
#
#     end add/mov/delmodebtn subs
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     toggle auto scroll state from UI
#
sub autoscrolltoggle{
if($btn_AutoScroll->get_active){
  $btn_AutoScroll->set_active(FALSE);
}else{
  $btn_AutoScroll->set_active(TRUE);
}
}
#
#     end autoscrolltoggle sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     two subs for opening the file chooser as open png
#     or save pdf
#
sub show_chooser_png{
  show_chooser($window,'Choose image file','open',ret_png_filter());
}
#----------------------------------------------------------------
sub show_chooser_pdf{
  show_chooser($window,'Choose output pdf file','save',ret_pdf_filter());
}
#
#     end show_chooser_png/df subs
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     toggle point position state from UI
#
sub togglepointposition{
if($btn_closestposition->get_active){
  $btn_closestposition->set_active(FALSE);
}else{
  $btn_closestposition->set_active(TRUE);
}
}
#
#     end togglepointposition
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#
#     main drawing area (ex menubar, toolbar and statusbar)
#
#
sub createmaindrawingarea {
#          hbox
my $hbox = Gtk3::HBox->new (FALSE, 0);
$hbox->set_border_width(5);

#          scolledwindow
my $vp = Gtk3::Viewport->new( undef, undef );
$ScrolledWindow = Gtk3::ScrolledWindow->new(undef, undef );
$ScrolledWindow->set_policy( 'automatic', 'automatic' );
$ScrolledWindow->add( $vp );

#           drawing area
$drawing_area = Gtk3::DrawingArea->new;
$drawing_area->set_size_request ($width*$scale,$height*$scale);

#           add the drawing area to the viewport
$vp->add($drawing_area);
$hbox->pack_start ($ScrolledWindow, TRUE, TRUE, 0);

# connect signals to the drawing area
$drawing_area->signal_connect (draw => \&cairo_draw);
$drawing_area->signal_connect (button_press_event => \&button_press_event);
$drawing_area->add_events ([qw/
button-press-mask
/]);

#$drawing_area->signal_connect (configure_event => \&configure_event);
#$drawing_area->signal_connect (motion_notify_event => \&motion_notify_event);
#$drawing_area->signal_connect (button_release_event => \&button_release_event);

#button-release-mask
#button-motion-mask
#leave-notify-mask
#exposure-mask
#pointer-motion-mask
#pointer-motion-hint-mask


# $drawing_area->set_extension_events("cursor");, including extension events
# so we get drawing signals from stylus if one is connected

#           activating all input devices
#
#my @devices = Gtk3::Gdk::DeviceManager->list_devices();
# gdk_device_manager_list_devices
#for(my $i=0;$i<$#devices;$i++){
#  if($debug==1){
#    my $name=$devices[$i]->name;
#    print "Name: $name\n";
#  }
#  my $result=$devices[$i]->set_mode('GDK_MODE_SCREEN');
#  if($debug==1){
#    print "Activation: $result\n";
#    my $mode=$devices[$i]->mode;
#    print "Mode: $mode\n";
#  }
#}

#          button box
$buttonbox = Gtk3::VBox->new (FALSE, 0);
$buttonbox->set_border_width(5);

#          Config button
$btn_config = Gtk3::Button->new ("Con_fig");
$btn_config->set_size_request($buttonwidth,$buttonheight);
$btn_config->signal_connect (clicked => \&configure, $window);
$buttonbox->add($btn_config);

#          Export
$btn_save = Gtk3::Button->new('_Export');
$btn_save->set_size_request($buttonwidth,$buttonheight);
$btn_save->signal_connect('clicked' => \&export);
$buttonbox->add($btn_save);

#          AutoScroll
$btn_AutoScroll = Gtk3::CheckButton->new("Auto_Scroll");
$btn_AutoScroll->set_active(TRUE);
$btn_AutoScroll->signal_connect('toggled' => \&toggleautoscrollbtn);
$buttonbox->add($btn_AutoScroll);

#          Draw Mode
$btn_drawmode = Gtk3::CheckButton->new("Draw m_ode");
$btn_drawmode->set_active(TRUE);
$btn_drawmode->signal_connect('toggled' => \&toggledrawmodebtn);
$buttonbox->add($btn_drawmode);

#          Color Mode
$btn_colormode = Gtk3::CheckButton->new("Color m_ode");
$btn_colormode->set_active(FALSE);
$btn_colormode->signal_connect('toggled' => \&togglecolormodebtn);
$buttonbox->add($btn_colormode);

#          Select Path
$btn_selectpath = Gtk3::CheckButton->new("Select _Path");
$btn_selectpath->set_active(FALSE);
$btn_selectpath->signal_connect('toggled' => \&toggleselectpathbtn);
$buttonbox->add($btn_selectpath);

#          Mode frame
$modeframe = Gtk3::Frame->new('Point Mode:');
$modeframe->set_size_request($framewidth,4*$buttonheight);
$modeframe->set_border_width(1);
my $vbox_modes = Gtk3::VBox->new(TRUE,0);
$vbox_modes->set_border_width(1);

#          Add, Delete and Move buttons
$btn_addmode = Gtk3::CheckButton->new("_Add");
$btn_delmode = Gtk3::CheckButton->new("_Delete");
$btn_movmode = Gtk3::CheckButton->new("_Move");
$btn_addmode->set_active(TRUE);
$btn_delmode->set_active(FALSE);
$btn_movmode->set_active(FALSE);
$btn_addmode->signal_connect('toggled' => \&addmodebtn);
$btn_delmode->signal_connect('toggled' => \&delmodebtn);
$btn_movmode->signal_connect('toggled' => \&movmodebtn);

$vbox_modes->pack_start($btn_addmode,FALSE,FALSE,0);
$vbox_modes->pack_start($btn_movmode,FALSE,FALSE,0);
$vbox_modes->pack_start($btn_delmode,FALSE,FALSE,0);
$modeframe->add($vbox_modes);
$buttonbox->add($modeframe);

#          Color frame
$colorframe = Gtk3::Frame->new('Color:');
$colorframe->set_size_request($framewidth,2*$buttonheight);
$colorframe->set_border_width(1);
my $vbox_colors = Gtk3::VBox->new(TRUE,0);
$vbox_colors->set_border_width(1);

#          Black and White buttons
$btn_blackmode = Gtk3::CheckButton->new("_Black");
$btn_whitemode = Gtk3::CheckButton->new("_White");
$btn_blackmode->set_active(TRUE);
$btn_whitemode->set_active(FALSE);
$btn_blackmode->signal_connect('toggled' => \&toggleblackmodebtn );
$btn_whitemode->signal_connect('toggled' => \&togglewhitemodebtn );
$vbox_colors->pack_start($btn_blackmode,FALSE,FALSE,0);
$vbox_colors->pack_start($btn_whitemode,FALSE,FALSE,0);
$colorframe->add($vbox_colors);
$buttonbox->add($colorframe);

#          Position Frame
$positionframe = Gtk3::Frame->new('Point Position:');
$positionframe->set_border_width(1);
$positionframe->set_size_request($framewidth,2.5*$buttonheight);
my $vbox_positions = Gtk3::VBox->new(TRUE,0);
$vbox_positions->set_border_width(1);

#          Any and Closest position buttons
$btn_anyposition = Gtk3::CheckButton->new("Any");
$btn_closestposition = Gtk3::CheckButton->new("Closest");
$btn_anyposition->set_active(FALSE);
$btn_closestposition->set_active(TRUE);
$btn_anyposition->signal_connect('toggled' => \&anypositionbtn);
$btn_closestposition->signal_connect('toggled' => \&closestpositionbtn);
$vbox_positions->pack_start($btn_anyposition,FALSE,FALSE,0);
$vbox_positions->pack_start($btn_closestposition,FALSE,FALSE,0);
$positionframe->add($vbox_positions);
$buttonbox->add($positionframe);

#          new path frame
$newpathframe = Gtk3::Frame->new("Start new path,\nmark current as:");
$newpathframe->set_size_request($framewidth,3.5*$buttonheight);
$newpathframe->set_border_width(1);
my $newpathbox = Gtk3::HBox->new (TRUE, 0);
$newpathbox->set_border_width(2);

#          start new path, mark current one as open
my $btn_newpath = Gtk3::Button->new('ope_n');
$btn_newpath->set_size_request($buttonwidth/2,$buttonheight);
$btn_newpath->signal_connect('clicked' => \&opennewpath,$window);
$newpathbox->add($btn_newpath);

#          start new path, mark current one as closed
my $btn_closepath = Gtk3::Button->new('_closed');
$btn_closepath->set_size_request($buttonwidth/2,$buttonheight);
$btn_closepath->signal_connect('clicked' => \&closenewpath,$window);
$newpathbox->add($btn_closepath);

$newpathframe->add($newpathbox);
$buttonbox->add($newpathframe);

# range box
my $rangebox = Gtk3::VBox->new(FALSE, 0);

# attach the circleradius scale
my $vscale = Gtk3::VScale->new($circleradius);
$vscale->set_size_request(40,200);
scale_set_default_values($vscale);
$rangebox->pack_start($vscale, TRUE, TRUE, 0);
$vscale->show;

# attach the degrees scale
my $vscaledeg = Gtk3::VScale->new($degrees);
$vscaledeg->set_size_request(40,200);
scale_set_default_values($vscaledeg);
$rangebox->pack_start($vscaledeg, TRUE, TRUE, 0);
$vscaledeg->show;

$rangebox->show;

# add button box on right hand side, make it stick to the top
my $valign=Gtk3::Alignment->new(0,0,0,0);
if($oldstyle==1){
  $valign->add($buttonbox);
}else{
  $valign->add($rangebox);
}

$hbox->pack_start ($valign, FALSE, FALSE, 0);

return $hbox;

}
#
#     end createdrawingarea sub
#
#----------------------------------------------------------------

sub set_linewidth_and_related{
  # print "Debug:".$linewidthslider->get_value()."\n";
  my $value=($linewidthslider->get_value()/100);
  $value=0.1+2*$value+8*$value**3;
  # main linewidth params
  $millimeter_width_for_export=0.9*$value;
  $millimeter_width=0.9*$value;
  # other variables derived from those
  $pwidth=$millimeter_width*$width/210;
  $linewidth=$millimeter_width*$width/210;
  $pointrad=$linewidth/4;  
  $longirange=$linewidth;
  $latirange=$linewidth;
  $minclosestdistance=$linewidth;
  # schedule a redraw if the drawing area exists (that is, we got called by moving the linewidth slider)
  if (defined $drawing_area){
    $drawing_area->queue_draw();
  }
}

#----------------------------------------------------------------
#
#     set default values for scale
#
sub scale_set_default_values
{
  my $scale = shift;
  $scale->set_digits(0);
  $scale->set_value_pos('top');
  $scale->set_draw_value(TRUE);
}
#
#     end scale_set_default_values sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     next two subs toggle the any and closest position
#     buttons. Since they are mutually exclusive, one unsets
#     the other
#
sub anypositionbtn {
  if($btn_anyposition->get_active){
    $btn_closestposition->set_active(FALSE);
  }else{
    if($oldstyle==1){
      $btn_closestposition->show;
    }
    $btn_closestposition->set_active(TRUE);
    $btn_anyposition->hide;
  }
}
#----------------------------------------------------------------
sub closestpositionbtn {
  if($btn_closestposition->get_active){
    $btn_anyposition->set_active(FALSE);
  }else{
    if($oldstyle==1){
      $btn_anyposition->show;
    }
    $btn_anyposition->set_active(TRUE);
    $btn_closestposition->hide;
  }
}
#
#     end any/closestposition subs
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#  configure_event sub: redraw the surface from the variables
#  set earlier. Useless and deprecated
#
#
sub configure_event {
my $widget = shift; # GtkWidget *widget
my $event = shift; # GdkEventConfigure *event
return TRUE;
}
#
#     end configure sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
# queue_drawing sub: schedule a redraw
#
#
sub queue_drawing {
  $drawing_area->queue_draw();
}
#
#     end queue_drawing sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
# cairo_draw sub: draw the whole contents
#
#
sub cairo_draw {
  my ( $widget, $context, $ref_status ) = @_;
  # set the background
  $context->scale($scale,$scale);
  $context->set_source_surface($keepsurface,0,0);
  $context->paint();
  # and now draw the contents
  redraw_all($context);
  return TRUE;
}
#
#     end cairo_draw sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
# manage clicks on the drawing area
#
#
sub button_press_event {
my $widget = shift; # GtkWidget *widget
my $event = shift; # GdkEventButton *event

if($#intensity==-1){
  @intensity=make_intensity_matrix($keepsurface);
}

# get pointer position and event position. These should (more or less) agree.
# If event position is too far from pointer position, use this instead of
# event position (useful for thinkpad button presses).
my ($x, $y, $mask) = $widget -> get_pointer();
my @eventcoords=($event->x,$event->y);
$eventcoords[0]=$eventcoords[0]/$scale;
$eventcoords[1]=$eventcoords[1]/$scale;
my @pointcoords=($x/$scale,$y/$scale);
my @newcoords=check_distance(\@pointcoords,\@eventcoords,$maxdist/$scale);

# will not accept new point if space distance from last recorded point is less
# than $mindistance pixels or previous record occured less than 0.5 seconds ago.
my $newtime=$event->time;
my $distance=distance(\@newcoords,\@lastpoint);
if(($distance<$mindistance/$scale) || ($newtime-$lasttime<500)){
  return TRUE;
}else{
  $lasttime=$newtime;
  @lastpoint=@newcoords;
}

# will register left clicks only
if ($event->button == 1) {

  if($btn_AutoScroll->get_active){
    set_scrolled_window_to_coords($newcoords[0]*$scale,$newcoords[1]*$scale);  # center scrolling on current point
  }

# replace current coordinates by those of an existing point, if one is found within small distance.
  if($btn_closestposition->get_active){
    @newcoords=replace_with_closest(\@newcoords);
  }
# replace current coordinates by those of predicted point, if it is found within small distance.
  if($predictX){
    if(distance(\@newcoords,[$predictX,$predictY])<$minclosestdistance){
      @newcoords=($predictX,$predictY);
    }
  }

# if we are not selecting path (=> we are adding points, or in the process of dropping a previously selected point for moving)
  if(!$btn_selectpath->get_active){
    # if we are in addmode
    if($btn_addmode->get_active){
      if($currentpos>=0){
        splice(@{$allX  [$currentpath]},$currentpos,0,$newcoords[0]);
        splice(@{$allY  [$currentpath]},$currentpos,0,$newcoords[1]);
        if($btn_blackmode->get_active){
          splice(@{$colors[$currentpath]},$currentpos,0,1);
        }else{
          splice(@{$colors[$currentpath]},$currentpos,0,0);
        }
        $currentpos++;
      }
    # if we are in movemode
    }else{
      if($currentpos>=0){
        splice(@{$allX  [$currentpath]},$currentpos,1,$newcoords[0]);
        splice(@{$allY  [$currentpath]},$currentpos,1,$newcoords[1]);
        $currentpos++;
        $btn_selectpath->set_active(TRUE);
        reset_lastpoint();
      }
    }
    $drawing_area->queue_draw();
  }else{
# we are in select path mode, so either we are coloring paths or we are deleting points => we need to get the path and point numbers
    ($currentpath,$currentpos)=get_current_values(\@newcoords);
    if(($btn_colormode->get_active) && ($currentpos>=0)){
      # set corresponding color
      if($btn_blackmode->get_active){
        splice(@{$colors[$currentpath]},$currentpos,1,1);
      }else{
        splice(@{$colors[$currentpath]},$currentpos,1,0);
      }
      $btn_selectpath->set_active(TRUE);
    }
    if($btn_delmode->get_active){
      # delete current point
      if($currentpos>=0){
        splice(@{$allX  [$currentpath]},$currentpos,1);
        splice(@{$allY  [$currentpath]},$currentpos,1);
        splice(@{$colors[$currentpath]},$currentpos,1);
        $currentpos--;
        reset_lastpoint();
      }
    }
    $drawing_area->queue_draw();
  }


  if($debug==1){                             # might want to do different thing depending on pointing
    my $device=$event->device;               # device used?
#    my $name=$device->name;
#    my $source=$device->source;
    print "$newcoords[0] $newcoords[1] from button 1 press\n";
  }
}
if ($event->button == 3) {          # useless (so far) might use it to erase points?
  if($debug==1){                    # maybe if eraser generates this event?
    my $device=$event->device;      # actually, eraser would be another device?
    my $name=$device->name;
    my $source=$device->source;
    print "$newcoords[0] $newcoords[1] from button 3 press $name $source\n";
  }
}
if ((($event->button >= 4) && ($event->button <= 7))) {
  if($debug==1){                       # it seems touchpad scrolling generates a button 4-7 push
    my $device=$event->device;         # followed by a string of button 4-7 releases.
    my $name=$device->name;            # will only start scrolling on the release events.
    my $source=$device->source;
    print "$newcoords[0] $newcoords[1] from button 4 press $name $source\n";
  }
}

return TRUE;
}
#
#     end button_press_event sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     replace coordinates by closest one found in our
#     paths if one is found at less than linewidth distance
#
#
sub replace_with_closest{
my ($coords)=@_;

  my ($closestX,$closestY);
  my $mindist=10000000;
  for(my $i=0;$i<$#allX+1;$i++){
    my @tX=@{$allX[$i]};
    my @tY=@{$allY[$i]};
    for(my $j=0;$j<$#tX+1;$j++){
      if(($i!=$currentpath) || ($j!=$currentpos)){
        my $ldist=distance($coords,[$tX[$j],$tY[$j]]);
        if($ldist<$mindist){
          $mindist=$ldist;
          $closestX=$tX[$j];
          $closestY=$tY[$j];
        }
      }
    }
  }

  if($mindist<$minclosestdistance){
    return ($closestX,$closestY);
  }else{
    return (@$coords);
  }
}
#
#     end replace_with_closest sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     find which point in which path is the one we clicked on
#
#
sub get_current_values{
my ($coords)=@_;

  my $pathcount;
  my $pointcount;
  my $mindist=10000000;
  for(my $i=0;$i<$#allX+1;$i++){
    my @tX=@{$allX[$i]};
    my @tY=@{$allY[$i]};
    for(my $j=0;$j<$#tX+1;$j++){
      my $ldist=distance($coords,[$tX[$j],$tY[$j]]);
      if($ldist<$mindist){
        $mindist=$ldist;
        $pathcount=$i;
        $pointcount=$j;
      }
    }
  }

  # if the distance is small enough, we don't need to be in selectpath mode anymore, unless we are in delete mode
  if($mindist<$mindistance){
    if(!$btn_delmode->get_active){
      $btn_selectpath->set_active(FALSE);
    }
    # if we are in addmode, the index of the next point we drop is one more than the current one
    if($btn_addmode->get_active){
      $pointcount++;
    }
    return ($pathcount,$pointcount);
  }else{
    return ($currentpath,$currentpos);
  }

}
#
#     end get_current_values
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     Manage button releases. A scroll on the right hand side
#     of the touchpad is interpreted a click followed by a
#     series of button releases
#
#
sub button_release_event {
my $widget = shift; # GtkWidget *widget
my $event = shift; # GdkEventButton *event

if ($event->button == 4) {           # touchpad vertical scrolling
  if($debug==1){
    my $device=$event->device;
    my $name=$device->name;
    my $source=$device->source;
    print "button release 4, $name $source\n";
  }
  my $adj = $ScrolledWindow->get_vadjustment ();
  inc_scrolled_window($adj,-1);
}
if ($event->button == 5) {           # touchpad vertical scrolling (other direction ;-)
  if($debug==1){
    my $device=$event->device;
    my $name=$device->name;
    my $source=$device->source;
    print "button release 5, $name $source\n";
  }
  my $adj = $ScrolledWindow->get_vadjustment ();
  inc_scrolled_window($adj,1);
}
if ($event->button == 6) {           # touchpad horizontal scrolling
  my $device=$event->device;
  my $name=$device->name;
  my $source=$device->source;
  if($debug==1){
    print "button release 6, $name $source\n";
  }
  my $adj = $ScrolledWindow->get_hadjustment ();
  inc_scrolled_window($adj,-1);
}
if ($event->button == 7) {           # touchpad horizontal scrolling (other direction ;-)
  my $device=$event->device;
  my $name=$device->name;
  my $source=$device->source;
  if($debug==1){
    print "button release 7, $name $source\n";
  }
  my $adj = $ScrolledWindow->get_hadjustment ();
  inc_scrolled_window($adj,1);
}

return TRUE;
}
#
#     end button_relase_event
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     correct pointer position on button press events
#
#
sub check_distance {                 # this sub compares two points in the plane
my ($v1,$v2)=@_;                     # the first point is the current pointer position
my ($x1,$y1)=@{$v1};                 # the second point is the last event position
my ($x2,$y2)=@{$v2};                 # most of the time these two agree, but, on my thinkpad,
my $dx=($x2-$x1);                    # when I click on a trackpad button while moving the
my $dy=($y2-$y1);                    # pointer with the touchpad instead of the trackpad (=red button in middle of the keyboard)
my $distance=sqrt($dx*$dx+$dy*$dy);  # then the button press event is reported as happening
my @nv;                              # in a weird place (negative coordinates, or random?).
if($distance>$maxdist){              # When this happens, the distance between the two points is large
  @nv =@{$v1};                       # so we return the pointer position instead of the
}else{                               # supposedly more accurate event position.
  @nv =@{$v2};
}
return(@nv);
}
#
#     end check_distance sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     compute distance between two points
#
#
sub distance {         # well, this sub could be used in the check_distance sub
my ($v1,$v2)=@_;       # this time we only return the distance...
my ($x1,$y1)=@{$v1};
my ($x2,$y2)=@{$v2};
my $dx=($x2-$x1);
my $dy=($y2-$y1);
my $distance=sqrt($dx*$dx+$dy*$dy);
return($distance);
}
#
#     end distance sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     manage mouse motion events (buggy, might not work)
#
#
sub motion_notify_event {                     # this is similar to the button_press_event sub
my $widget = shift; # GtkWidget *widget       # and is where it is important to record new points
my $event = shift; # GdkEventMotion *event    # only in case of sufficient distance from last point
                                              # because wacom pen events are actually emitted as
my ($x, $y, $state);                          # motion events, and would add thousand of points
if ($event->is_hint) {                        # to our path...
  (undef, $x, $y, $state) = $event->window->get_pointer;
} else {
  $x = $event->x;
  $y = $event->y;
  $state = $event->state;
}
if ($state >= "button1-mask") {
  my ($px, $py, $mask) = $widget->get_pointer();
  my @eventcoords=($x,$y);
  my @pointcoords=($px,$py);
  my @newcoords=check_distance(\@pointcoords,\@eventcoords,$maxdist);

  my $newtime=$event->time;
  my $distance=distance(\@newcoords,\@lastpoint);
  if(($distance<$mindistance) || ($newtime-$lasttime<500)){
    return TRUE;
  }else{
    $lasttime=$newtime;
    @lastpoint=@newcoords;
  }

  if($btn_AutoScroll->get_active){
    set_scrolled_window_to_coords(@newcoords);  # center scrolling on current point
  }

  if($debug==1){
    print "$newcoords[0], $newcoords[1] from motion\n";
    my $device=$event->device;
#    my $name=$device->name;
#    my $source=$device->source;
    print "$newcoords[0] $newcoords[1] from motion\n";
  }
}
return TRUE;
}
#
#     end motion_notify_event sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     import points from previous runs
#
#
sub myimport{


my $intensityfile=$pngname."_intensity";
if(-e "$intensityfile"){
  @intensity = @{csv (in => $intensityfile,sep_char=> " ")};
}
my $intensityfilegz=$pngname."_intensity.gz";
if((-e "$intensityfilegz") && ($#intensity<0)){
  my $gz=gzopen($intensityfilegz,"rb");
  my $alldata;
  my $ldata;
  while($gz->gzread($ldata)>0){
    $alldata.=$ldata;
  }
  $gz->gzclose;
  my $pintensity;
  eval $alldata;
  @intensity=@{$pintensity};
}
my $pointsfile=$pngname."_points_v1.gz";
if(-e "$pointsfile"){
  my $gz=gzopen($pointsfile,"rb");
  my $alldata;
  my $ldata;
  while($gz->gzread($ldata)>0){
    $alldata.=$ldata;
  }
  $gz->gzclose;
  
  @allX=();
  @allY=();
  @colors=();
  @closed=();
  foreach my $line (split(/\n/,$alldata)){
    if ($line=~ /pathX/){
      my $pathX;
      my $pathY;
      my $pcolors;
      my $pclosed;
      eval $line;      
      push(@allX,$pathX);
      push(@allY,$pathY);
      push(@colors,$pcolors);
      push(@closed,$pclosed);      
    }else{
     eval $line;
    }
  }
  
  $currentpos=0;
  push(@allX,[]);
  push(@allY,[]);
  push(@colors,[]);
  $currentpath=$#allX;
  $closed[$currentpath]=0;
  
}else{
  @allX=();         # will contain all X coordinates of our paths
  @allY=();         # and Y coordinates
  @closed=();       # will contain flags to denote open or closed path
  @colors=();       # will contain black/white flag or segments in our paths
  $currentpath=0;   # index of path being currently modified
  $currentpos=0;    # position of point being currently modified

  $closed[0]=0;     # by default paths are open
  push(@allX,[]);   # start populating the paths
  push(@allY,[]);   # and colors with
  push(@colors,[]); # anonymous arrays
}
reset_lastpoint();
}
#
#     end myimport sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     convert a path (=X array, Y array, Color array and Closed status
#     into a string that can be eval'ed to recover those values
#
#
sub path_to_string {
  my ($pcX,$pcY,$pcc,$closed)=@_;
  my @currentX=@{$pcX};
  my @currentY=@{$pcY};
  my @currentcolors=@{$pcc};
  
  my $outX ="\$pathX=[".join( ',', @currentX)."]; ";
  my $outY ="\$pathY=[".join( ',', @currentY)."]; ";
  my $outcolor ="\$pcolors=[".join( ',', @currentcolors)."]; ";
  my $outclosed="\$pclosed=$closed;";

  return $outX.$outY.$outcolor.$outclosed;
    
}
#
#     end path_to_string sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     export to pdf file, and also save points to gz file
#
#
sub export{

  my $pointsfile=$pngname."_points_v1.gz";
  my $gz=gzopen($pointsfile,"wb");
  for (my $pathcount=0;$pathcount<$#allX+1;$pathcount++){
    my @currentX=@{$allX[$pathcount]};
    my @currentY=@{$allY[$pathcount]};
    my @currentcolors=@{$colors[$pathcount]};
    if($#currentX>0){ # keep path with at least 2 members
      my $ldata=path_to_string(\@currentX,\@currentY,\@currentcolors,$closed[$pathcount]);    
      $gz->gzwrite($ldata);
      $gz->gzwrite("\n");
    }
  }
  # keep track of the current path and current position
  $gz->gzwrite("\$currentpath=$currentpath;\n\$currentpos=$currentpos;\n");
  # keep track of the circle/sector radiue, the sector opening and the linewidth
  my $def_val=$circleradius->get_value();
  $gz->gzwrite("\$circleradius_default=$def_val\n");
  $def_val=$degrees->get_value();
  $gz->gzwrite("\$degrees_default=$def_val\n");
  $def_val=$linewidthslider->get_value();
  $gz->gzwrite("\$linewidth_default=$def_val;\n");
  $gz->gzclose;

  # A4 paper has standard size 595x842 in whatever units
  my $pssurface = Cairo::PdfSurface->create ($pdfname, 595, 842);

  # but in millimeters, the width is 210mm
  my $linewidth_for_export=$millimeter_width_for_export*595/210;
  my $pointrad=$linewidth/2;

  # scale all the points so they occupy a max of the A4 page
  my ($pX,$pY)=ps_scale(\@allX,\@allY);

  my @cX=@$pX;
  my @cY=@$pY;

  # fill the page as white
  my $cr = Cairo::Context->create( $pssurface );
  $cr->set_source_rgba(1.0, 1.0, 1.0, 1);
  $cr->rectangle(0,0,595,842);
  $cr->fill;

  # switch linewidth to pdf linewidth
  my $linewidthkeep=$linewidth;
  $linewidth=$linewidth_for_export;
  $withpoints=0;
  for(my $i=0;$i<$#cX+1;$i++){
    my $mX=$cX[$i];
    my $mY=$cY[$i];
    draw_curve($cr,$mX,$mY,$closed[$i],0,$colors[$i]);
  }
  $withpoints=1;
  # revert linewidth to UI value
  $linewidth=$linewidthkeep;


  $cr->show_page;
  $pssurface->flush;

  # need to do this so the pdf file is flushed ?????
  $cr=undef;
  $pssurface=undef;

  # open pdf file, works at least in linux, if okular and which are installed
  if($Config{osname} eq 'linux'){
    my $okular=`which okular`;
    if($okular !~ /Command not found./){
      system("okular $pdfname");
    }
  }else{
    system("$pdfname");
  }
}
#
#     end export sub
#
#----------------------------------------------------------------



#----------------------------------------------------------------
#
#     create configure dialog.
#
#
sub configure{
  my $config = Gtk3::Window->new ();
  # this is a child of our main window
  $config->set_transient_for ($window);
  $config->set_destroy_with_parent (TRUE);
  
  $config->set_title ("scribble settings");
  $config->set_size_request(300,-1);
  $config->signal_connect('key-press-event' => \&proc_key_destroy,$config);

  # a box to hold our sliders and buttons
  my $buttonbox = Gtk3::VBox->new (FALSE, 0);
  $buttonbox->set_border_width(5);
  $config->add($buttonbox);

  #          Apply and Close button box
  # my $firstbuttonbox = Gtk3::HBox->new (FALSE, 0);
  # $firstbuttonbox->set_border_width(5);

  #          Input dialog
  # my $btn_input = Gtk3::Button->new ("_Input Dialog");
  # $btn_input->set_size_request(1.5*$buttonwidth,$buttonheight);
  # $btn_input->signal_connect (clicked => \&create_input_dialog, $config);
  # $btn_input->show;

  #my $haligna=Gtk3::Alignment->new(0,0,0,0);
  #$haligna->add($firstbuttonbox);
  #$firstbuttonbox->add($btn_input);

  #$buttonbox->add($haligna);

  #          a frame to hold the sector/circle radius slider
  my $circleframe = Gtk3::Frame->new('Sector/Circle radius:');
  $circleframe->set_border_width(1);
  #          a vbox to pack in the frame
  my $vbox_circle = Gtk3::VBox->new(TRUE,0);
  $vbox_circle->set_border_width(1);
  #          and a scale to pack in the vbox
  my $hscale = Gtk3::HScale->new($circleradius);
  $hscale->set_size_request(200,40);
  scale_set_default_values($hscale);
  $hscale->set_value_pos('bottom');
  $vbox_circle->add($hscale);
  $hscale->show;
  $circleframe->add($vbox_circle);

  #          a frame to hold the sector/circle opening slider
  my $sectorframe = Gtk3::Frame->new('Sector opening (in degrees):');
  $sectorframe->set_border_width(1);
  #          a vbox to pack in the frame
  my $vbox_sector = Gtk3::VBox->new(TRUE,0);
  $vbox_sector->set_border_width(1);
  #          and a scale to pack in the vbox
  $hscale = Gtk3::HScale->new($degrees);
  $hscale->set_size_request(200,40);
  scale_set_default_values($hscale);
  $hscale->set_value_pos('bottom');
  $vbox_sector->add($hscale);
  $hscale->show;
  $sectorframe->add($vbox_sector);

  #          a frame to hold the slinewidth slider
  my $linewidthframe = Gtk3::Frame->new('Linewidth:');
  #          a vbox to pack in the frame
  $linewidthframe->set_border_width(1);
  my $vbox_linewidth = Gtk3::VBox->new(TRUE,0);
  $vbox_linewidth->set_border_width(1);
  #          and a scale to pack in the vbox
  $hscale = Gtk3::HScale->new($linewidthslider);
  $hscale->set_size_request(200,40);
  scale_set_default_values($hscale);
  $hscale->set_value_pos('bottom');
  $vbox_linewidth->add($hscale);
  $hscale->show;
  $linewidthframe->add($vbox_linewidth);

  #          add all three frames with sliders to the buttonbox
  $buttonbox->add($circleframe);
  $buttonbox->add($sectorframe);
  $buttonbox->add($linewidthframe);

  #          Apply and Close button box
  my $lastbuttonbox = Gtk3::HBox->new (FALSE, 0);
  $lastbuttonbox->set_border_width(5);

  #          Close button
  my $btn_quit = Gtk3::Button->new_from_stock('gtk-close');
  $btn_quit->signal_connect_swapped (clicked => sub { $_[0]->destroy; }, $config);

  #          Apply button not needed as we redraw as the sliders move.
  #          If we need to, we could connect it to something and use it.
  my $btn_apply = Gtk3::Button->new_from_stock('gtk-apply');
  
  #          "Default values" button resets to the hardwired default values.
  my $btn_reset = Gtk3::Button->new_with_label('default values');
  $btn_reset->signal_connect(clicked => \&sliders_set_to_defaults, $config);

  my $halign=Gtk3::Alignment->new(1,0,0,0);
  $halign->add($lastbuttonbox);
  $lastbuttonbox->add($btn_apply);
  $lastbuttonbox->add($btn_reset);
  $lastbuttonbox->add($btn_quit);

  my $valign=Gtk3::Alignment->new(1,1,0,0);
  $valign->add($halign);

  $buttonbox->add($valign);

  $config->show_all;

  # hide the apply button for now, as it is not connected anyway.
  $btn_apply->hide;

}
#
#     end configure sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     create input dialog (and hide useless "save" button)
#
#
sub create_input_dialog{

my $dialog = Gtk3::InputDialog->new();

my $vbox=$dialog->get_children;
my $buttonbox=(($vbox->get_children))[2];
my @child=($buttonbox->get_children);
my $save_button=$child[0];
my $close_button=$child[1];
$save_button->hide;

$close_button->signal_connect( clicked => sub { $_[0]->destroy; }, $dialog);
$dialog->show;

$dialog->signal_connect('key-press-event' => \&proc_key_destroy,$dialog);

return $dialog;
}
#
#     end create_input_dialog sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     scroll, baby scroll (small increments)
#
#
sub inc_scrolled_window {
my ($adj,$direction)= @_;

my ($h_upper, $h_page_size) = $adj->get ('upper', 'page-size');
my $newh = min(max($adj->get_value+$direction*($h_upper-$h_page_size)/20,0),$h_upper-$h_page_size);
$adj->set_value ($newh);
}
#
#     end inc_scrolled_window sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     scroll again, big increments
#
#
sub scroll_page {
my ($adj,$direction)= @_;
my ($h_upper, $h_page_size) = $adj->get ('upper', 'page-size');
my $newh = min(max($adj->get_value+$direction*$h_page_size*0.8,0),$h_upper-$h_page_size);
$adj->set_value ($newh);
}
#
#     end scroll_page sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     zoom in and out on our Cairo surface
#
sub zoomin{
  $scale=$scale*1.1;
  $drawing_area->queue_draw(); 
}
#----------------------------------------------------------------
sub zoomout{
  $scale=$scale/1.1;
  $drawing_area->queue_draw();
}
#
#     end zoomin/out subs
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     cut functions
#
#
sub longicut {
my ($x,$range)=@_;
my $y=exp(-$x*$x*6/$range/$range);
return($y);
}
#----------------------------------------------------------------
sub laticut {
my ($x,$range)=@_;
my $y=1;
if(abs($x)>$range){
  $y=0;
}
return($y);
}
#
#     end cut functions
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     manage key presses
#
#
sub proc_key {
  my ($widget,$event,$parameter)= @_;
  my $key_val = $event->keyval();

  # catch Esc or q to exit
  if( ($key_val == Gtk3::Gdk::KEY_Escape) || ($key_val == Gtk3::Gdk::KEY_q) )
      { Gtk3->main_quit; }

  #right arrow scolling
  if($key_val == Gtk3::Gdk::KEY_Right){
    my $adj = $ScrolledWindow->get_hadjustment ();
    inc_scrolled_window($adj,1);
    return TRUE;
  }

  #up arrow scolling
  if($key_val == Gtk3::Gdk::KEY_Up){
    my $adj = $ScrolledWindow->get_vadjustment ();
    inc_scrolled_window($adj,-1);
    return TRUE;
  }

  #down arrow scolling
  if($key_val == Gtk3::Gdk::KEY_Down){
    my $adj = $ScrolledWindow->get_vadjustment ();
    inc_scrolled_window($adj,1);
    return TRUE;
  }

  #left arrow scolling
  if($key_val == Gtk3::Gdk::KEY_Left){
    my $adj = $ScrolledWindow->get_hadjustment ();
    inc_scrolled_window($adj,-1);
    return TRUE;
  }

    #page up scolling
  if($key_val == Gtk3::Gdk::KEY_Page_Up){
    my $adj = $ScrolledWindow->get_vadjustment ();
    scroll_page($adj,-1);
    return TRUE;
  }

  #page down scolling
  if($key_val == Gtk3::Gdk::KEY_Page_Down){
    my $adj = $ScrolledWindow->get_vadjustment ();
    scroll_page($adj,1);
    return TRUE;
  }

  # set black mode
  if($key_val == Gtk3::Gdk::KEY_b){
    if(!$btn_blackmode->get_active){
      $btn_blackmode->set_active(TRUE);
    }else{
      $btn_whitemode->set_active(TRUE);
    }
  }
  # set white mode
  if($key_val == Gtk3::Gdk::KEY_w){
    if(!$btn_whitemode->get_active){
      $btn_whitemode->set_active(TRUE);
    }else{
      $btn_blackmode->set_active(TRUE);
    }
  }

  # zoom in
  if($key_val == Gtk3::Gdk::KEY_plus){
    zoomin();
  }

  # zoom out
  if($key_val == Gtk3::Gdk::KEY_minus){
    zoomout();
  }

  # start new path, mark current one as open
  if($key_val == Gtk3::Gdk::KEY_n){

    $closed[$currentpath]=0;
    $currentpos=0;
    push(@allX,[]);
    push(@allY,[]);
    push(@colors,[]);
    $currentpath=$#allX;
    $closed[$currentpath]=0;

    reset_lastpoint();

    $btn_addmode->set_active(TRUE);
    $btn_selectpath->set_active(FALSE);

    update_statusbar();
    update_toolbar();

    $drawing_area->queue_draw();
    return TRUE;
  }

  # start new path, mark current one as closed
  if($key_val == Gtk3::Gdk::KEY_c){

    $closed[$currentpath]=1;
    $currentpos=0;
    push(@allX,[]);
    push(@allY,[]);
    push(@colors,[]);
    $currentpath=$#allX;
    $closed[$currentpath]=0;

    reset_lastpoint();

    $btn_addmode->set_active(TRUE);
    $btn_selectpath->set_active(FALSE);

    update_statusbar();
    update_toolbar();

    $drawing_area->queue_draw();
    return TRUE;
  }

  # adjust the next point clicked to the "best" close point according to intensity
  if($key_val == Gtk3::Gdk::KEY_a){
    # we are moving a point, so we need to be in move mode and select path
    $btn_movmode->set_active(TRUE);
    $btn_selectpath->set_active(TRUE);
    update_statusbar();
    update_toolbar();
    if($#intensity==-1){
      # just in case we do not have an intensity matrix yet
      @intensity=make_intensity_matrix($keepsurface);
    }

    if($currentpos>-1){
      my @locX=@{$allX[$currentpath]};
      my @locY=@{$allY[$currentpath]};

      if($#locX>0){

        my ($origX,$origY)=($allX[$currentpath][$currentpos],$allY[$currentpath][$currentpos]);
        if((!$origX) || (!$origY)){
          return TRUE;
        }

        my ($rfcpX,$rfcpY,$rscpX,$rscpY);
        if($closed[$currentpath]==1){
          ($rfcpX,$rfcpY,$rscpX,$rscpY)=GetCurveControlPointsClosed(\@locX,\@locY);
        }else{
          ($rfcpX,$rfcpY,$rscpX,$rscpY)=GetCurveControlPoints(\@locX,\@locY);
        }
        my ($tX,$tY);
        my @fcpX=@{$rfcpX};
        my @fcpY=@{$rfcpY};
        if($currentpos<$#locX+1){
          $tX=$fcpX[$currentpos];
          $tY=$fcpY[$currentpos];
          if(($btn_movmode->get_active) && ($currentpos==$#locX) && ($closed[$currentpath]==0)){
            my @scpX=@{$rscpX};
            my @scpY=@{$rscpY};
            $tX=2*$origX-$scpX[-1];
            $tY=2*$origY-$scpY[-1];
          }
          if($btn_addmode->get_active){
            $tX=$fcpX[$currentpos-1];
            $tY=$fcpY[$currentpos-1];
          }
        }else{
          my @scpX=@{$rscpX};
          my @scpY=@{$rscpY};
          if($closed[$currentpath]==0){
            $tX=2*$origX-$scpX[-1];
            $tY=2*$origY-$scpY[-1];
          }else{
            $tX=0*$origX+$fcpX[-1];
            $tY=0*$origY+$fcpY[-1];
          }
        }

        my $u=($tX-$origX);
        my $v=($tY-$origY);
        my $len=sqrt($u*$u+$v*$v);
        $u=$u/$len;
        $v=$v/$len;


        if($debug==1){
          print "Debug: path\#: $currentpath point \#: $currentpos coords: $origX $origY\n";
        }
        my $rX=sprintf('%.0f',$origX);
        my $rY=sprintf('%.0f',$origY);

        my $delta=2*max($latirange,$longirange);

        my ($mX,$mY,$wei)=(0,0,0);
        for(my $i=max($rX-$delta,0);$i<min($rX+$delta+1,$width);$i++){
          for(my $j=max($rY-$delta,0);$j<min($rY+$delta+1,$height);$j++){
            my $fac=laticut((-$v*($i-$rX)+$u*($j-$rY)),$latirange)*longicut(($u*($i-$rX)+$v*($j-$rY)),$longirange);

            $mX+=$intensity[$j][$i]*$i*$fac;
            $mY+=$intensity[$j][$i]*$j*$fac;
            $wei+=$intensity[$j][$i]*$fac;
          }
        }

        if($wei>0){

          $mX=$mX/$wei;
          $mY=$mY/$wei;
          splice(@{$allX  [$currentpath]},$currentpos,1,$mX);
          splice(@{$allY  [$currentpath]},$currentpos,1,$mY);

          $drawing_area->queue_draw();
          if($debug==1){
            print "weighted: $mX,$mY ";
          }
        }
        if($debug==1){
          print "original: $origX,$origY\n";
        }
      }
    }
  }

  # key=1=northwest corner adjustment
 if($key_val == Gtk3::Gdk::KEY_1){
    scroll_to_corner('northwest');
  }

  # key=2=northeast corner adjustment
  if($key_val == Gtk3::Gdk::KEY_2){
    scroll_to_corner('northeast');
  }

  # key=3=southeast corner adjustment
  if($key_val == Gtk3::Gdk::KEY_3){
    scroll_to_corner('southeast');
  }

  # key=4=southwest corner adjustment
  if($key_val == Gtk3::Gdk::KEY_4){
    scroll_to_corner('southwest');
  }

  return FALSE;
}
#
#     end proc_key sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     mark current path as open, start new path
#
#
sub opennewpath {
my ($widget)=@_;
  $closed[$currentpath]=0;
  $currentpos=0;
  push(@allX,[]);
  push(@allY,[]);
  push(@colors,[]);
  $currentpath=$#allX;
  $closed[$currentpath]=0;

  reset_lastpoint();

  $btn_addmode->set_active(TRUE);
  $btn_selectpath->set_active(FALSE);

  update_statusbar();
  update_toolbar();

  $drawing_area->queue_draw();
  return TRUE;
}
#
#     end newpath sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     mark current path as closed, start new path
#
#
sub closenewpath {
my ($widget)=@_;
  $closed[$currentpath]=1;
  $currentpos=0;
  push(@allX,[]);
  push(@allY,[]);
  push(@colors,[]);
  $currentpath=$#allX;
  $closed[$currentpath]=0;

  reset_lastpoint();

  $btn_addmode->set_active(TRUE);
  $btn_selectpath->set_active(FALSE);

  update_statusbar();
  update_toolbar();

  $drawing_area->queue_draw();
  return TRUE;
}
#
#     end closepath sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     draw all paths
#
#
sub redraw_all {
  my ($cr)=@_;

  # draw all the curves first
  for(my $i=0;$i<$#allX+1;$i++){
    my $currentflag=0;
    if($i==$currentpath){
      $currentflag=1;
    }
    draw_curve($cr,$allX[$i],$allY[$i],$closed[$i],$currentflag,$colors[$i]);
  }
  
  $predictX= undef;
  $predictY= undef;
  if(($btn_drawmode->get_active) && ($withpoints==1) && ($currentpos>-1) && ($btn_addmode->get_active || ($btn_movmode->get_active && !$btn_selectpath->get_active))){
    my @locX=@{$allX[$currentpath]};
    my @locY=@{$allY[$currentpath]};
    if($#locX>-1){
      my $circrad=$circleradius->get_value;
      # get the coordinates of the current point
      my ($cx,$cy);
      if($btn_addmode->get_active){
        ($cx,$cy)=($allX[$currentpath][$currentpos-1],$allY[$currentpath][$currentpos-1]);
      }
      if($btn_movmode->get_active){
        ($cx,$cy)=($allX[$currentpath][$currentpos],$allY[$currentpath][$currentpos]);
      }
      
      if(($#locX==0) && ($btn_addmode->get_active)){
        # there is only one point in our path
        $cr->set_source_rgba(0.3,0.3,0.3,1);
        $cr->set_line_width($linewidth/4);
        $cr->arc ($cx,$cy,$circrad,0,2*$pi);
        $cr->stroke;
        
        
        # how far to look around
        my $delta=sprintf('%.0f',1.4*max($latirange,$longirange));

        my $maxwei=0;
        my ($bestX,$bestY);
        for(my $deg=0;$deg<361;$deg++){
          # a circle around our current point
          my $rX=sprintf('%.0f',$cx+$circrad*cos($deg/180*$pi));
          my $rY=sprintf('%.0f',$cy+$circrad*sin($deg/180*$pi));
          # tangent vector to the circle
          my $u=cos(($deg/180-1/2)*$pi);
          my $v=sin(($deg/180-1/2)*$pi);

          # compute weighted average with intensity
          my ($mX,$mY,$wei)=(0,0,0);
          for(my $i=max($rX-$delta,0);$i<min($rX+$delta+1,$width);$i++){
            for(my $j=max($rY-$delta,0);$j<min($rY+$delta+1,$height);$j++){
              # weight of current point, cut to 0 outside of interesting region
              my $fac=laticut((-$v*($i-$rX)+$u*($j-$rY)),$latirange)*longicut(($u*($i-$rX)+$v*($j-$rY)),$longirange);

              $mX+=$intensity[$j][$i]*$i*$fac;
              $mY+=$intensity[$j][$i]*$j*$fac;
              $wei+=$intensity[$j][$i]*$fac;
            }
          }

          if($wei>$maxwei){
            # this point has a higher intensity than met before, so we record it
            $maxwei=$wei;
            $bestX=$mX/$wei;
            $bestY=$mY/$wei;
          }
        }
        if($maxwei>0){
          # there was at least a point with a positive intensity
          # so we plot it (in gray)
          $cr->arc ($bestX,$bestY,3*$pointrad,0,2 * $pi);
          $cr->fill;
          # and we set it as our next predicted point
          $predictX=$bestX;
          $predictY=$bestY;
        }
        
        
        
        
        
      
      }
      if($#locX>0){
        # our curve has several points
        my ($rfcpX,$rfcpY,$rscpX,$rscpY);
        if($closed[$currentpath]==1){
          ($rfcpX,$rfcpY,$rscpX,$rscpY)=GetCurveControlPointsClosed(\@locX,\@locY);
        }else{
          ($rfcpX,$rfcpY,$rscpX,$rscpY)=GetCurveControlPoints(\@locX,\@locY);
        }
        my ($tX,$tY);
        my @fcpX=@{$rfcpX};
        my @fcpY=@{$rfcpY};
        if($currentpos<$#locX+1){
          # tangent direction to the curve
          $tX=$fcpX[$currentpos];
          $tY=$fcpY[$currentpos];
          if(($btn_movmode->get_active) && ($currentpos==$#locX) && ($closed[$currentpath]==0)){
            my @scpX=@{$rscpX};
            my @scpY=@{$rscpY};
            $tX=2*$cx-$scpX[-1];
            $tY=2*$cy-$scpY[-1];
          }
          if($btn_addmode->get_active){
            $tX=$fcpX[$currentpos-1];
            $tY=$fcpY[$currentpos-1];
          }
        }else{
          my @scpX=@{$rscpX};
          my @scpY=@{$rscpY};
            if($closed[$currentpath]==0){
              $tX=2*$cx-$scpX[-1];
              $tY=2*$cy-$scpY[-1];
            }else{
              $tX=0*$cx+$fcpX[-1];
              $tY=0*$cy+$fcpY[-1];
            }
        }

        if($btn_addmode->get_active){
          # change the pen color to light gray and small linewidth
          $cr->set_source_rgba(0.3,0.3,0.3,1);
          $cr->set_line_width($linewidth/4);

          # end of vector starting at current point, tangent to curve there and of length $circrad
          my $len=sqrt(($tX-$cx)*($tX-$cx)+($tY-$cy)*($tY-$cy));
          $tX=$cx+($tX-$cx)/$len*$circrad;
          $tY=$cy+($tY-$cy)/$len*$circrad;

          # angle of said vector wrt x-axis
          my $angle=atan2($tY-$cy,$tX-$cx);
          my $deg=$degrees->get_value;

          # draw the opening of the sector (pie slice)
          $cr->move_to($cx,$cy);
          $cr->line_to($cx+$circrad*cos($angle+$deg/180*$pi),$cy+$circrad*sin($angle+$deg/180*$pi));
          $cr->stroke;
          $cr->move_to($cx,$cy);
          $cr->line_to($cx+$circrad*cos($angle-$deg/180*$pi),$cy+$circrad*sin($angle-$deg/180*$pi));
          $cr->stroke;
 
          # draw the boundary of the sector
          $cr->arc ($cx,$cy,$circrad,$angle-$deg/180*$pi,$angle+$deg/180*$pi);
          $cr->stroke;

          
          # start to look for best point along the sector's boundary
          # how far to look around
          my $delta=sprintf('%.0f',1.4*max($latirange,$longirange));

          # sector opening
          my $maxang=$degrees->get_value;

          # we'll look for 100=2*50 different angle values
          my $maxdeg=50;
          my $maxwei=0;
          my ($bestX,$bestY);
          for(my $deg=-$maxdeg;$deg<$maxdeg+1;$deg++){
            # a point on the sector
            my $rX=sprintf('%.0f',$cx+$circrad*cos($angle+($maxang*$deg/$maxdeg/180)*$pi));
            my $rY=sprintf('%.0f',$cy+$circrad*sin($angle+($maxang*$deg/$maxdeg/180)*$pi));
            # and its corresponding tangent vector
            my $u=cos($angle+($maxang*$deg/$maxdeg/180-1/2)*$pi);
            my $v=sin($angle+($maxang*$deg/$maxdeg/180-1/2)*$pi);

            # compute intensity weighted average around the point on the sector
            my ($mX,$mY,$wei)=(0,0,0);
            for(my $i=max($rX-$delta,0);$i<min($rX+$delta+1,$width);$i++){
              for(my $j=max($rY-$delta,0);$j<min($rY+$delta+1,$height);$j++){
                my $fac=laticut((-$v*($i-$rX)+$u*($j-$rY)),$latirange)*longicut(($u*($i-$rX)+$v*($j-$rY)),$longirange);

                $mX+=$intensity[$j][$i]*$i*$fac;
                $mY+=$intensity[$j][$i]*$j*$fac;
                $wei+=$intensity[$j][$i]*$fac;
              }
            }

            if($wei>$maxwei){
              # this point has a higher intensity than met before, so we record it
              $maxwei=$wei;
              $bestX=$mX/$wei;
              $bestY=$mY/$wei;
            }
          }
          if($maxwei>0){
            # there was at least a point with a positive intensity
            # so we plot it (in gray)
            $cr->arc ($bestX,$bestY,3*$pointrad,0,2 * $pi);
            $cr->fill;
            # and we set it as our next predicted point
            $predictX=$bestX;
            $predictY=$bestY;
          }
        }

        if($btn_movmode->get_active){
          # if we are moving mode, we draw a rectangle around the current point (but, why?)
          my $u=($tX-$cx);
          my $v=($tY-$cy);
          my $len=sqrt($u*$u+$v*$v);
          $u=$u/$len;
          $v=$v/$len;

          my $rX=sprintf('%.0f',$cx);
          my $rY=sprintf('%.0f',$cy);

          $cr->set_source_rgba(1.0,0,0,1);
          $cr->set_line_width(1);
          $cr->move_to($rX+0.6194*$longirange*$u+$latirange*$v,$rY+0.6194*$longirange*$v-$latirange*$u);
          $cr->line_to($rX+0.6194*$longirange*$u-$latirange*$v,$rY+0.6194*$longirange*$v+$latirange*$u);
          $cr->line_to($rX-0.6194*$longirange*$u-$latirange*$v,$rY-0.6194*$longirange*$v+$latirange*$u);
          $cr->line_to($rX-0.6194*$longirange*$u+$latirange*$v,$rY-0.6194*$longirange*$v-$latirange*$u);
          $cr->line_to($rX+0.6194*$longirange*$u+$latirange*$v,$rY+0.6194*$longirange*$v-$latirange*$u);
          $cr->stroke;
        }

      }

    }
  }
  # display the page
  $cr->show_page;
}
#
#     end redraw_all sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     manage key presses in "input dialog" sub-window
#
#
sub proc_key_destroy {
  my ($widget,$event,$window)= @_;
  my $key_val = $event->keyval();

  # catch Esc or q to exit
  if( ($key_val == Gtk3::Gdk::KEY_Escape) || ($key_val == Gtk3::Gdk::KEY_q) )
      { $window->destroy; }

  #good practice to let the event propagate, should we need it somewhere else
  return FALSE;
}
#
#     end proc_key_destroy sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     set scroll to max value
#
#
sub set_adj_to_max {
    my $adj = shift;
    my ($upper, $page_size) = $adj->get ('upper', 'page-size');
    $adj->set_value ($upper - $page_size);
}
#
#     end set_adj_to_max sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     set scroll to min value
#
#
sub set_adj_to_min {
    my $adj = shift;
    $adj->set_value ($adj->get ('lower'));
}
#
#     end set_adj_to_min sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     scroll to all four corners of the drawing area
#
#
sub scroll_to_corner {
    my $which = shift;

    my $hadj = $ScrolledWindow->get_hadjustment ();
    my $vadj = $ScrolledWindow->get_vadjustment ();

    if ($which eq 'northwest') {
        set_adj_to_min ($hadj);
        set_adj_to_min ($vadj);

    } elsif ($which eq 'northeast') {
        set_adj_to_max ($hadj);
        set_adj_to_min ($vadj);

    } elsif ($which eq 'southeast') {
        set_adj_to_max ($hadj);
        set_adj_to_max ($vadj);

    } elsif ($which eq 'southwest') {
        set_adj_to_min ($hadj);
        set_adj_to_max ($vadj);
    }
}
#
#     end scroll_to_corner sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     scroll to center window on pointer position
#     (only if it is possible)
#
#
sub set_scrolled_window_to_coords {
my ($x,$y)= @_;

my $hadj = $ScrolledWindow->get_hadjustment ();
my $vadj = $ScrolledWindow->get_vadjustment ();

my ($h_upper, $h_page_size) = $hadj->get ('upper', 'page-size');
my ($v_upper, $v_page_size) = $vadj->get ('upper', 'page-size');

if($x+$h_page_size/2<$width*$scale){
  my $newh = max($x-$h_page_size/2,0);
  $hadj->set_value ($newh);
}else{
  $hadj->set_value ($h_upper-$h_page_size);
}
if($y+$v_page_size/2<$height*$scale){
  my $newv = max($y-$v_page_size/2,0);
  $vadj->set_value ($newv);
}else{
  $vadj->set_value ($v_upper-$v_page_size);
}
}
#
#     end set_scrolled_window_to_coords sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     draw one path
#
#
sub draw_curve{
my ($cr,$pX,$pY,$closeflag,$currentflag,$pcolors)=@_;

my ($rfcpX,$rfcpY,$rscpX,$rscpY);
my @X=@$pX;
my @Y=@$pY;
my @colors=@$pcolors;

  # if there is only one point
  if($#X<1){
    # and we are drawing on screen
    if($withpoints==1){
      $cr->set_source_rgba(1.0, 0.0, 0.0, 1);
      for(my $i=0;$i<$#X+1;$i++){
        # set the color according to the selectpath state
        if(($currentflag==1) && ((($i==$currentpos) && ($btn_movmode->get_active)) || (($i==$currentpos-1) && ($btn_addmode->get_active))) && (!$btn_selectpath->get_active)){
          $cr->set_source_rgba(0.0, 0.0, 1.0, 1);
        }else{
          $cr->set_source_rgba(1.0, 0.0, 0.0, 1);
        }
        #draw the point
        $cr->arc ($X[$i],$Y[$i],3*$pointrad,0,2 * $pi);
        $cr->fill;
      }
    }
    return;
  }

  # get the Bezier "first" and "second" control points (code is different if path is closed or open
  if($closeflag==1){
    ($rfcpX,$rfcpY,$rscpX,$rscpY)=GetCurveControlPointsClosed($pX,$pY);
  }else{
    ($rfcpX,$rfcpY,$rscpX,$rscpY)=GetCurveControlPoints($pX,$pY);
  }

  my @fcpX=@$rfcpX;
  my @fcpY=@$rfcpY;
  my @scpX=@$rscpX;
  my @scpY=@$rscpY;

  $cr->set_source_rgba(0.0, 0.0, 0.0, 1);
  $cr->set_line_width($linewidth);
  $cr->set_line_cap('round');

  $cr->move_to($X[0],$Y[0]);

# handle closed curve case. condition below could be replaced by $closeflag==1 ;-)
  if($#X==$#fcpX){
    push(@X,$X[0]);
    push(@Y,$Y[0]);
  }

  for(my $i=0;$i<$#fcpX+1;$i++){
    # if we are adding points inside an existing path (and not at the end), highlight the segment in green
    if(($currentflag==1) && ($i==$currentpos-1) && ($btn_addmode->get_active) && (!$btn_colormode->get_active)){
      $cr->set_source_rgba(0.0, 1.0, 0.0, 1);
    }else{
      $cr->set_source_rgba(0.0, 0.0, 0.0, 1);
    }

    # white segments are drawn in gray with half linewidth on screen (so we know where they are)
    $cr->set_line_width($linewidth);
    if($withpoints==1){
      if($colors[min($#colors,$i+1)]==0){
        $cr->set_source_rgba(0.5, 0.5, 0.5, 1);
        $cr->set_line_width($linewidth/2);
      }
    }

    # draw a Bezier segment
    if(($colors[min($#colors,$i+1)]==1) || ($withpoints==1)){
      $cr->curve_to($fcpX[$i],$fcpY[$i],$scpX[$i],$scpY[$i],$X[$i+1],$Y[$i+1]);
      $cr->stroke;
    }
    $cr->move_to($X[$i+1],$Y[$i+1]);
  }


  # if we draw on screen, we add points so we can identify them later (to move or delete, for instance)
  if($withpoints==1){
    $cr->set_source_rgba(1.0, 0.0, 0.0, 1);
    for(my $i=0;$i<$#X+1;$i++){
      # the "current" point is drawn in blue, but "current" index depends on whether the path is closed or not
      my $loccurrentpos=$currentpos;
      if(($btn_movmode->get_active) && ($currentpos==0) && ($closeflag==1)){
        $loccurrentpos=$#X;
      }
      if(($btn_addmode->get_active) && ($currentpos==1) && ($closeflag==1)){
        $loccurrentpos=$#X+1;
      }
      if(($currentflag==1) && ((($i==$loccurrentpos) && ($btn_movmode->get_active)) || (($i==$loccurrentpos-1) && ($btn_addmode->get_active))) && (!$btn_selectpath->get_active)){
        $cr->set_source_rgba(0.0, 0.0, 1.0, 1);
      }else{
        $cr->set_source_rgba(1.0, 0.0, 0.0, 1);
      }
      # draw point
      $cr->arc ($X[$i],$Y[$i],3*$pointrad,0,2 * $pi);
      $cr->fill;
    }
    # add a small white sector to indicate in which direction the path is growing
    # we use the Bezier "first" control points to know the tangent to the path at the given point
    $cr->set_source_rgba(1.0, 1.0, 1.0, 1);
    for(my $i=0;$i<$#X;$i++){
      my $angle=atan2($fcpY[$i]-$Y[$i],$fcpX[$i]-$X[$i])+$pi;
      $cr->move_to($X[$i],$Y[$i]);
      $cr->arc ($X[$i],$Y[$i],3*$pointrad,$angle-0.7,$angle+0.7);
      $cr->fill;
    }
    # for the last point of the path, we use the Bezier "second" control points from the last segment for the tangent
    my $i=$#X;
    my $angle=atan2($scpY[$i-1]-$Y[$i],$scpX[$i-1]-$X[$i]);
    $cr->move_to($X[$i],$Y[$i]);
    $cr->arc ($X[$i],$Y[$i],3*$pointrad,$angle-0.7,$angle+0.7);
    $cr->fill;
  }

}
#
#     end draw_curve
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     compute control points for path (open case)
#
#
sub GetCurveControlPoints{
my ($rknotsX,$rknotsY)=@_;
my @knotsX=@$rknotsX;
my @knotsY=@$rknotsY;
my $n=$#knotsX;

my @firstControlPointsX=();
my @firstControlPointsY=();
my @secondControlPointsX=();
my @secondControlPointsY=();


if($n<1){
  die "Bezier: at least two points required\n\n";
}elsif($n==1){

  $firstControlPointsX[0] = (2 * $knotsX[0] + $knotsX[1]) / 3;
  $firstControlPointsY[0] = (2 * $knotsY[0] + $knotsY[1]) / 3;

  $secondControlPointsX[0] = 2 * $firstControlPointsX[0] - $knotsX[0];
  $secondControlPointsY[0] = 2 * $firstControlPointsY[0] - $knotsY[0];
}else{
  my @rhs=@knotsX;
  for(my $i=1;$i<$n-1;++$i){
    $rhs[$i] = 4 * $knotsX[$i] + 2 * $knotsX[$i + 1];
  }
  $rhs[0] = $knotsX[0] + 2 * $knotsX[1];
  $rhs[$n-1] = (8 * $knotsX[$n-1] + $knotsX[$n]) / 2;
  my @x = GetFirstControlPoints(@rhs);

  @rhs=@knotsY;
  for(my $i=1;$i<$n-1;++$i){
    $rhs[$i] = 4 * $knotsY[$i] + 2 * $knotsY[$i + 1];
  }
  $rhs[0] = $knotsY[0] + 2 * $knotsY[1];
  $rhs[$n-1] = (8 * $knotsY[$n-1] + $knotsY[$n]) / 2;
  my @y = GetFirstControlPoints(@rhs);

  for(my $i=0;$i<$n;++$i){
    $firstControlPointsX[$i] = $x[$i];
    $firstControlPointsY[$i] = $y[$i];
    if($i<$n-1){
      $secondControlPointsX[$i]=2*$knotsX[$i+1]-$x[$i+1];
      $secondControlPointsY[$i]=2*$knotsY[$i+1]-$y[$i+1];
    }else{
      $secondControlPointsX[$i]=($knotsX[$n]+$x[$n-1])/2;
      $secondControlPointsY[$i]=($knotsY[$n]+$y[$n-1])/2;
    }
  }
}

return(\@firstControlPointsX,\@firstControlPointsY,\@secondControlPointsX,\@secondControlPointsY);
}
#
#     end GetCurveControlPoints
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     get "first" Bezier control points (derivative at t=0)
#     open case
#
#
sub GetFirstControlPoints{
my (@rhs)=@_;
my $n = $#rhs;
my @x = ();
my @tmp = ();

my $b = 2;
$x[0] = $rhs[0] / $b;
for(my $i=1;$i<$n+1;$i++){
  $tmp[$i] = 1 / $b;
  my $c;
  if($i<$n-1){
    $c=4;
  }else{
    $c=7/2;
  }
  $b = $c - $tmp[$i];
  $x[$i] = ($rhs[$i] - $x[$i - 1]) / $b;
}
for(my $i=1;$i<$n;$i++){
  $x[$n - $i - 1] = $x[$n - $i - 1] - $tmp[$n - $i]* $x[$n - $i];
}
return @x;
}
#
#     end GetFirstControlPoints
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     compute control points for path (closed case)
#
#
sub GetCurveControlPointsClosed{
my ($rknotsX,$rknotsY)=@_;
my @knotsX=@$rknotsX;
my @knotsY=@$rknotsY;
my $n=$#knotsX;

my @firstControlPointsX=();
my @firstControlPointsY=();
my @secondControlPointsX=();
my @secondControlPointsY=();


if($n<1){
  die "Bezier: at least two points required\n\n";
}elsif($n==1){

  $firstControlPointsX[0] = (2 * $knotsX[0] + $knotsX[1]) / 3;
  $firstControlPointsY[0] = (2 * $knotsY[0] + $knotsY[1]) / 3;

  $secondControlPointsX[0] = 2 * $firstControlPointsX[0] - $knotsX[0];
  $secondControlPointsY[0] = 2 * $firstControlPointsY[0] - $knotsY[0];
}else{
  my @rhs1X=();
  my @rhs2X=();
  for(my $i=0;$i<$n;++$i){
    $rhs1X[$i] = 4 * $knotsX[$i] + 2 * $knotsX[$i+1];
  }
  $rhs1X[$n]= 4 * $knotsX[$n] + 2 * $knotsX[0];

  my @rhs1Y=();
  my @rhs2Y=();
  for(my $i=0;$i<$n;++$i){
    $rhs1Y[$i] = 4 * $knotsY[$i] + 2 * $knotsY[$i+1];
  }
  $rhs1Y[$n]= 4 * $knotsY[$n] + 2 * $knotsY[0];

  @firstControlPointsX=GetFirstControlPointsClosed(@rhs1X);
  @firstControlPointsY=GetFirstControlPointsClosed(@rhs1Y);

  for(my $i=0;$i<$n;++$i){
    $secondControlPointsX[$i]=2*$knotsX[$i+1]-$firstControlPointsX[$i+1];
    $secondControlPointsY[$i]=2*$knotsY[$i+1]-$firstControlPointsY[$i+1];
  }
  $secondControlPointsX[$n]=2*$knotsX[0]-$firstControlPointsX[0];
  $secondControlPointsY[$n]=2*$knotsY[0]-$firstControlPointsY[0];

}

return(\@firstControlPointsX,\@firstControlPointsY,\@secondControlPointsX,\@secondControlPointsY);
}
#
#     end GetCurveControlPointsClosed
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     get "first" Bezier control points (derivative at t=0)
#     closed case
#
#
sub GetFirstControlPointsClosed{
my (@b)=@_;
my $N = $#b+1;
my @x;
my @z;
my @c;
my @alpha;
my @gamma;
my @delta;

if ($N == 1){
  $x[0] = $b[0]/4;
}

$alpha[0] = 4;
$gamma[0] = 1 / $alpha[0];
$delta[0] = 1 / $alpha[0];

for (my $i = 1; $i < $N - 2; $i++){
  $alpha[$i] = 4 - $gamma[$i - 1];
  $gamma[$i] = 1 / $alpha[$i];
  $delta[$i] = -$delta[$i - 1] / $alpha[$i];
}

my $sum=0;
for (my $i = 0; $i < $N - 2; $i++){
  $sum += $alpha[$i] * $delta[$i] * $delta[$i];
}

$alpha[$N - 2] = 4 - $gamma[$N - 3];
$gamma[$N - 2] = (1 - $delta[$N - 3]) / $alpha[$N - 2];
$alpha[$N - 1] = 4 - $sum - $alpha[$N - 2] * $gamma[$N - 2] * $gamma[$N - 2];

$z[0] = $b[0];
for (my $i = 1; $i < $N - 1; $i++){
  $z[$i] = $b[$i] - $z[$i - 1] * $gamma[$i - 1];
}
$sum = 0;
for (my $i = 0; $i < $N - 2; $i++){
  $sum += $delta[$i] * $z[$i];
}

$z[$N - 1] = $b[$N - 1] - $sum - $gamma[$N - 2] * $z[$N - 2];
for (my $i = 0; $i < $N; $i++){
  $c[$i] = $z[$i] / $alpha[$i];
}

$x[$N - 1] = $c[$N - 1];
$x[$N - 2] = $c[$N - 2] - $gamma[$N - 2] * $x[$N - 1];
if ($N >= 3){
  for (my $i = $N - 3, my $j = 0; $j <= $N - 3; $j++, $i--){
    $x[$i] = $c[$i] - $gamma[$i] * $x[$i + 1] - $delta[$i] * $x[$N - 1];
  }
}

return @x;
}
#
#     end GetFirstControlPointsClosed
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     file chooser dialog
#
#
sub show_chooser {
#---------------------------------------------------
#Pops up a standard file chooser--------------------
#Specify a header to be displayed-------------------
#Specify a type depending on your needs-------------
#Optionally add a filter to show only certain files-
#will return a path, if valid----------------------
#---------------------------------------------------

    my($window,$heading,$type,$filter) =@_;
#$type can be:
#* 'open'
#* 'save'
#* 'select-folder'
#* 'create-folder'
    my $file_chooser =  Gtk3::FileChooserDialog->new (
                            $heading,
                            $window,
                            $type,
                            'gtk-cancel' => 'cancel',
                            'gtk-ok' => 'ok'
                        );

    (defined $filter)&&($file_chooser->add_filter($filter));

    #if action = 'save' suggest a filename
    ($type eq 'save')&&($file_chooser->set_current_name($pdfname));

    my $filename;

    if ('ok' eq $file_chooser->run){
       $filename = $file_chooser->get_filename;
    }

    $file_chooser->destroy;

    if (defined $filename){
        if ((-f $filename)&&($type eq 'save')) {
            my $overwrite =show_message_dialog( $window,
                                                'question'
                                                ,'Overwrite existing file:'."<b>\n$filename</b>"
                                                ,'yes-no'
                                    );
            return  if ($overwrite eq 'no');
        }
        if($type eq 'save'){
          $pdfname=$filename;
          # export to pdf, save the paths
          export();
        }
        if($type eq 'open'){
          $pngname=$filename;
          $pdfname=$pngname;
          $pdfname=~ s/\.[\w\W]+/\.pdf/g;

          # create our surface to hold the contents of the png file
          $keepsurface= Cairo::ImageSurface->create_from_png($pngname);
          # keep track of its size          
          $width=$keepsurface->get_width;
          $height=$keepsurface->get_height;
          $stride=$keepsurface->get_stride;
          $cformat=$keepsurface->get_format;

          # derived constants (point width, line width and point radius
          $pwidth=$millimeter_width*$width/210;
          $linewidth=$millimeter_width*$width/210;
          $pointrad=$linewidth/4;

          $scale=1;

          $drawing_area->set_size_request ($width*$scale,$height*$scale);
          
          # import paths and intensity matrix from previous runs if they exist
          myimport();
          # we might have changed default values during setup, so we set our sliders
          # to the new values (if needed).
          sliders_setup();

          if($#intensity==-1){
            # compute intensity matrix if not already done
            @intensity=make_intensity_matrix($keepsurface);
          }

          # schedule the drawing
          $drawing_area->queue_draw();
        }
    }
    return;
}
#
#     end show_chooser
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     simple dialog
#
#
sub show_message_dialog {
#---------------------------------------------------
#you tell it what to display, and how to display it
#$parent is the parent window, or "undef"
#$icon can be one of the following: a) 'info'
#                   b) 'warning'
#                   c) 'error'
#                   d) 'question'
#$text can be pango markup text, or just plain text, IE the message
#$button_type can be one of the following:  a) 'none'
#                       b) 'ok'
#                       c) 'close'
#                       d) 'cancel'
#                       e) 'yes-no'
#                       f) 'ok-cancel'
#---------------------------------------------------

my ($parent,$icon,$text,$button_type) = @_;

my $dialog = Gtk3::MessageDialog->new_with_markup ($parent,
                    [qw/modal destroy-with-parent/],
                    $icon,
                    $button_type,
                    sprintf "$text");
    my $retval = $dialog->run;
    $dialog->destroy;
    return $retval;
}
#
#     end show_message_dialog
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     filter for png/pdf files
#
#
sub ret_png_filter {
    my $filter = Gtk3::FileFilter->new();
    $filter->set_name("Images");
    $filter->add_mime_type("image/png");

    return $filter;
}
#----------------------------------------------------------------
sub ret_pdf_filter {
    my $filter = Gtk3::FileFilter->new();
    $filter->set_name("PDF");
    $filter->add_mime_type("application/pdf");

    return $filter;
}
#
#     end ret_png/pdf_filter sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     scale (and rotate) all points so that drawing takes
#     maximal size on A4 pdf file
#
#
sub ps_scale{
my ($pX,$pY)=@_;
my @X=@$pX;
my @Y=@$pY;


# unroll all points so we can compute min/max values
my @allX=();
my @allY=();
for(my $i=0;$i<$#X+1;$i++){
  my $lX=$X[$i];
  my $lY=$Y[$i];
  push(@allX,@$lX);
  push(@allY,@$lY);
}

# get min/max values and max width/height needed
my ($minx, $maxx) = minmax @allX;
my ($miny, $maxy) = minmax @allY;
my $dx=$maxx-$minx;
my $dy=$maxy-$miny;
my $rotate=0;

# if width is bigger than height, swap x and y (we want a portrait pdf file at the end)
if($dx>$dy){
  $rotate=1;
  my @kX=@X;
  my @kallX=@allX;
  @X=@Y;
  @Y=@kX;
  my $kdx=$dx;
  $dx=$dy;
  $dy=$kdx;
  my $kminx=$minx;
  my $kmaxx=$maxx;
  $minx=$miny;
  $maxx=$maxy;
  $miny=$kminx;
  $maxy=$kmaxx;
}

# adjust the scale so that we fill 80% of the max distance along the page
my $pscale;
my $scale;
if($dy<$dx/595*842){
  $pscale=595*8/10;
  $scale=$dx;
}else{
  $pscale=842*8/10;
  $scale=$dy;
}
for(my $j=0;$j<$#X+1;$j++){
  my $lX=$X[$j];
  my $lY=$Y[$j];
  my @llX=@$lX;
  my @llY=@$lY;
  for(my $i=0;$i<$#llX+1;$i++){
    $llX[$i]=297.5+($llX[$i]-($minx+$maxx)/2)*$pscale/$scale;
    # if rotate=1, we have swapped x and y, so we need a - sign on y to complete the rotation
    if($rotate==0){
      $llY[$i]=421+($llY[$i]-($miny+$maxy)/2)*$pscale/$scale;
    }else{
      $llY[$i]=421-($llY[$i]-($miny+$maxy)/2)*$pscale/$scale;
    }
  }
  $X[$j]=\@llX;
  $Y[$j]=\@llY;
}

return (\@X,\@Y);
}
#
#     end ps_scale sub
#
#----------------------------------------------------------------



#----------------------------------------------------------------
#
# This function registers our custom toolbar icons, so they can
# called later on (or be themed).
#
my $registered = FALSE;  # we want to do it only once?
sub register_stock_icons {
  if (!$registered) {
      my @items = (
        {
           stock_id => "scribble-open-path",
           label => "mark path as open",
        },
        {
           stock_id => "scribble-closed-path",
           label => "mark path as closed",
        },
        {
           stock_id => "scribble-add-mode",
           label => "add point to path",
        },
        {
           stock_id => "scribble-del-mode",
           label => "delete point from path",
        },
        {
           stock_id => "scribble-move-path",
           label => "move point in path",
        },
        {
           stock_id => "scribble-add-mode-sel",
           label => "add point to path",
        },
        {
           stock_id => "scribble-del-mode-sel",
           label => "delete point from path",
        },
        {
           stock_id => "scribble-move-path-sel",
           label => "move point in path",
        },
        {
           stock_id => "scribble-select-path",
           label => "Select Path",
        },
        {
           stock_id => "scribble-select-path-sel",
           label => "Select Path",
        },
      );

      $registered = TRUE;

      # Register our stock items
#      Gtk3::Stock_add (@items);
#      https://github.com/dave-theunsub/gtk3-perl-demos/blob/master/appwindow.pl

      # Add our custom icon factory to the list of defaults
      my $factory = Gtk3::IconFactory->new;
      $factory->add_default;

      # get the icons from the base64 encoding at the end of this file
      my ($scribbleaddicon,$scribbleadd_selicon,$scribbleblackicon,$scribbleblack_selicon,$scribbleclosedicon,$scribbleclosed_selicon,$scribblecoloricon,$scribblecolor_selicon,$scribbledeleteicon,$scribbledelete_selicon,$scribbledrawicon,$scribbledraw_selicon,$scribblemoveicon,$scribblemove_selicon,$scribbleopenicon,$scribbleopen_selicon,$scribbleselectpathicon,$scribbleselectpath_selicon,$scribblewhiteicon,$scribblewhite_selicon)=initicons();

      my ($filename,$pixbuf,$transparent,$icon_set);

      #                    "open path" icon
      $filename = "icons/open.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleopenicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-open-path", $icon_set);

      #                    "closed path" icon
      $filename = "icons/closed.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleclosedicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-closed-path", $icon_set);

      #                    "add point" icon (unselected)
      $filename = "icons/add.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleaddicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-add-mode", $icon_set);

      #                    "delete point" icon (unselected)
      $filename = "icons/delete.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbledeleteicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-del-mode", $icon_set);

      #                    "move point" icon (unselected)
      $filename = "icons/move.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribblemoveicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-move-mode", $icon_set);

      #                    "add point" icon (selected)
      $filename = "icons/add_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleadd_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-add-mode-sel", $icon_set);

      #                    "delete point" icon (selected)
      $filename = "icons/delete_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbledelete_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-del-mode-sel", $icon_set);

      #                    "move point" icon (selected)
      $filename = "icons/move_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribblemove_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-move-mode-sel", $icon_set);

      #                    "white mode" icon (unselected)
      $filename = "icons/white.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribblewhiteicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-white-mode", $icon_set);

      #                    "black mode" icon (unselected)
      $filename = "icons/black.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleblackicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-black-mode", $icon_set);

      #                    "white mode" icon (selected)
      $filename = "icons/white_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribblewhite_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-white-mode-sel", $icon_set);

      #                    "black mode" icon (selected)
      $filename = "icons/black_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleblack_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-black-mode-sel", $icon_set);

      #                    "select path" icon (unselected)
      $filename = "icons/selectpath.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleselectpathicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-select-path", $icon_set);

      #                    "select path" icon (selected)
      $filename = "icons/selectpath_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbleselectpath_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-select-path-sel", $icon_set);

      #                    "draw mode" icon (unselected)
      $filename = "icons/draw.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbledrawicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-draw-mode", $icon_set);

      #                    "draw mode" icon (selected)
      $filename = "icons/draw_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribbledraw_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-draw-mode-sel", $icon_set);

      #                    "color mode" icon (unselected)
      $filename = "icons/color.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribblecoloricon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-color-mode", $icon_set);

      #                    "color mode" icon (selected)
      $filename = "icons/color_sel.png";
      if(-e $filename){
        $pixbuf = Gtk3::Gdk::Pixbuf->new_from_file ($filename);
      }else{
        $pixbuf=$scribblecolor_selicon;
      }
      $transparent = $pixbuf->add_alpha (TRUE, 0xff, 0xff, 0xff); # make white background transparent
      $icon_set = Gtk3::IconSet->new_from_pixbuf ($transparent);
      $factory->add ("scribble-color-mode-sel", $icon_set);

  }
}
#
#     end register_stock_icons sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     show statusbar message depending on current state
#
sub update_statusbar {

  $statusbar->pop (0); # clear any previous message, underflow is allowed
  if($btn_drawmode->get_active){
    if(($btn_movmode->get_active) && ($btn_selectpath->get_active)){
      $statusbar->push (0, "   Choose point to be moved");
    }
    if(($btn_movmode->get_active) && (!$btn_selectpath->get_active)){
      $statusbar->push (0, "   Click where point is to be moved");
    }
    if(($btn_delmode->get_active)){
      $statusbar->push (0, "   Choose point to be deleted");
    }
    if(($btn_addmode->get_active) && ($btn_selectpath->get_active)){
      $statusbar->push (0, "   Choose point after which new point(s) will be added");
    }
    if(($btn_addmode->get_active) && (!$btn_selectpath->get_active)){
      $statusbar->push (0, "   Click on location of point to be added");
    }
  }else{
    if($btn_blackmode->get_active){
      $statusbar->push (0, "   Choose point at start of segment to be marked as black");
    }else{
      $statusbar->push (0, "   Choose point at start of segment to be marked as white");
    }
  }
}
#
#     end update_statusbar sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     next two sub update the menu/toolbar
#     the idea is first to remove the existing UI bar
#     then to get the "bare" UI info for the relevant bar
#     then change the words to reflect the current state
#     then re-insert the UI bar. We need to do this as the
#     menus change depending on the mode we are in.
sub update_menubar {
  $ui->remove_ui($menubar_magic);
  my $ui_menubar=$ui_info_menubar;
  if($btn_AutoScroll->get_active){
    $ui_menubar=~ s/AutoScroll/AutoScrollTrue/;
  }else{
    $ui_menubar=~ s/AutoScroll/AutoScrollFalse/;
  }

  $menubar_magic=$ui->add_ui_from_string ($ui_menubar);
}
#----------------------------------------------------------------
sub update_toolbar {

  $ui->remove_ui($toolbar_magic);
  my $ui_info_toolbar;
  if($btn_drawmode->get_active){
    $ui_info_toolbar=$ui_info_toolbar_drawmode;
    $ui_info_toolbar=~ s/DrawMode/DrawModeSel/;
    if($btn_addmode->get_active){
      $ui_info_toolbar=~ s/AddMode/AddModeSel/;
    }
    if($btn_movmode->get_active){
      $ui_info_toolbar=~ s/MoveMode/MoveModeSel/;
    }
    if($btn_delmode->get_active){
      $ui_info_toolbar=~ s/DelMode/DelModeSel/;
    }
    if($btn_selectpath->get_active){
      $ui_info_toolbar=~ s/SelectPath/SelectPathSel/;
    }
  }else{
    $ui_info_toolbar=$ui_info_toolbar_colormode;
    $ui_info_toolbar=~ s/ColorMode/ColorModeSel/;
    if($btn_whitemode->get_active){
      $ui_info_toolbar=~ s/WhiteMode/WhiteModeSel/;
    }
    if($btn_blackmode->get_active){
      $ui_info_toolbar=~ s/BlackMode/BlackModeSel/;
    }
  }

  $toolbar_magic=$ui->add_ui_from_string ($ui_info_toolbar);
}
#
#     end update_menu/toolbar subs
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     compute intensity matrix
#
sub make_intensity_matrix{
  # get the data
  my ($pixbuf)=@_;
  my $pixels=$pixbuf->get_data();
  # how many colors per pixel (rgb or rgba)
  my $depth = $pixbuf->get_stride/$pixbuf->get_width;
  # this will hold the intensity
  my @matrix=();
  my $height=$pixbuf->get_height();
  # length of one raw of data
  my $rowstride=$pixbuf->get_stride();

  # hide the status bar to display a progressbar instead
  $statusbar->hide;

  my $vbox = Gtk3::VBox->new(FALSE,0);
  $vbox->set_border_width(1);
  $vbox->show;

# Create a centering alignment object;
  my $align = Gtk3::Alignment->new(0.5, 0.5, 0, 0);
  $vbox->pack_start($align, FALSE, FALSE,1);
  $align->show;

# Create the Gtk3::ProgressBar and attach it to the window reference.
  my $ProgressBar = Gtk3::ProgressBar->new;
  $ProgressBar->set_text('computing intensity matrix, please wait...');
  $ProgressBar->set_show_text(TRUE);

# add the progress bar to the alignment object
  $align->add($ProgressBar);
  $ProgressBar->show;
  $vbox->show_all;

# add the vbox to the main table
  $table->attach ($vbox,0,1,3,4,[qw/expand fill/],[],0,0);

  my $size=$window->size_request();
  $ProgressBar->set_size_request($size->width-12,20);

  for(my $row=0;$row<$height;$row++){
    # go over the rows of data
    $ProgressBar->set_fraction($row/($height-1));
    Glib::MainContext->default->iteration(FALSE);
    
    # add an anonymous array
    push(@matrix,[]);
    # get (unpack) the current row of data
    my $offset = $row * ($rowstride) ;
    my @line=unpack "C*",substr $pixels, $offset, $rowstride+1;

    my $intensity=0;
    my $dc=0;
    # add together the rgb/rgba value for each pixel
    foreach my $color (@line){
      $dc=$dc+1;
      if($dc<=$depth){
        $intensity+=255-$color;
      }
      if($dc==$depth){
        $dc=0;
        push(@{$matrix[$row]},$intensity);
        $intensity=0;
      }
    }
  }

  # save the matrix to a (space-separated) csv file
  csv (in => \@matrix, out => $pngname."_intensity",sep_char=> " ");
  
  if ($debug==1){
    # print the intensity matrix to a matrix_matlab.m file
    # that can be used to display a contour plot to check 
    # the above is reasonable
    print_matrix(\@matrix);
  }

  $vbox->hide;
  $statusbar->show;

  return @matrix;
}
#
#     end make_intensity_matrix sub
#
#----------------------------------------------------------------

#----------------------------------------------------------------
#
#     print intensity matrix to matlab file for debugging
#
sub print_matrix{
  my ($ma)=@_;
  my @matrix=@{$ma};
  open(TXT,">matrix_matlab.m");
  print TXT "a=[";
  for(my $i=0;$i<$#matrix+1;$i++){
    my @line=@{$matrix[$i]};
    foreach my $entry (@line){
      print TXT "$entry ";
    }
    print TXT ";\n";
  }
  print TXT "];\n";
  print TXT "contour(a(end:-1:1,1));";
  close(TXT);
}
#
#     end print_matrix sub
#
#----------------------------------------------------------------


#----------------------------------------------------------------
#
#     To ship a single file, the icons are embedded in this
#     sub in a base64 string encoding a compressed data string.
#     So to get the pixbuf, we need to decode and decompress
#     the string, then feed it to
#
#          Gtk3::Gdk::Pixbuf->new_from_data
#
sub initicons{

#          "add mode" icon (unselected)
my $scribbleadd= <<EOscribbleadd;
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
ICZ6JSW6hB+W36BQ4zt+b4cs+t7j/wB3H+S4
EOscribbleadd

$scribbleadd = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleadd))  ,'rgb',0,8,92,77,276);

#          "add mode" icon (selected)
my $scribbleadd_sel= <<EOscribbleadd_sel;
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
EOscribbleadd_sel

$scribbleadd_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleadd_sel))  ,'rgb',0,8,92,77,276);

#          "black mode" icon (unselected)
my $scribbleblack= <<EOscribbleblack;
eJztnE2LglAYhfvnTYvaCgOVEgTRRDBEVlOrFq37+Bm1LOoP5By8cBGPRjNkpp1nZdf32rkPaW7u
GwRvwfl83mw20+n0KwQH+IjBvHPlw+FwgISPFHAKBXlnfB7X63W1WtVqtTQhBhSgDMV5580crNH3
/djyG43GZwgOYqdQXHoty+UyuuRWq4WR7Xa7C8EBPmIwWoORvFNnyH6/t7cMDvAb2KWAU9FKTMw7
e1b0+/3oTZEmxGqxxZhoL3I6nUajkeu6uNc8zxsOh9+vCrIhIXIiLTIjeUzI8Xi0a2y327eFGFBm
p2A6LjKbzW4/mV8c5I86Wa/X9hQeEfc4iT588N4yn8+r1Sp/UeJg7qRFXSwW1slkMjHj9XrdPlRv
gzIUm1l4nXvacrLGvpQOBgMz4jjOPUIMKDaz7PQSgJ+HcdLr9cwInjn3O0GxmWWnlwA8JzNyUikO
seTNZlNOYsm73a6cxJKPx2M5iSXHf6icyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4yc
MHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLC
yAkjJ4ycMDaz2RAnJxXty0gillz7dypP3OdVXLLbD1hctG+UeeD+4mLtQ0/k4fvQA/UroH4F5jqm
r4Xnea7r4k/N9/2fVwXZkBBRO51OYl+Ly+ViF/iPvhaYHpSRh/Q/KRnqk5OI+ikxaX23nJD37LsV
qD9bOurjl8af+j3+Agg/pg0=
EOscribbleblack

$scribbleblack = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleblack))  ,'rgb',0,8,92,77,276);

#          "black mode" icon (selected)
my $scribbleblack_sel= <<EOscribbleblack_sel;
eJztnMGK2lAUhn2m6Wa676K7obQPMR1o6XTplEllumoptIKYIAjBijCIUauzceFan0OXir6A9u/c
4SL5k8EWYzTzf9yF3pwTz/00Jpt71usnwWKxGI/HnU7n1z14gbeYTLuudJhOp5DwOQYcQkDaNe6P
1Wo1HA4LhUKcEAMCEIbgtOtNHKwxCILQ8vNf8u++v8fAi9AhBGdey2Aw2Fzy2x8XL25fnvRPT+7u
R/8UbzG5GYOUtKtOkMlkYi+Z68L1K//NgwoaOOQUHHsRITHt2pOiVqvZb//Mfx0nxAwE2GAk2pPM
5/Nms+m6brFY9Dyv0WjcHiqoDRWiTlSLmlF5SMhsNrNrPP958bgQM843LiKk4yTdbvfxf+YDB/Vv
OhmNRvbQ3/+QLZwgzKbguaXX6zmOwx8UOZk6caX2+33rpN1um/n8zdWzu+fbOEHY1c0nk4XHub0t
J2nsQ2m9XjczH75ebiPEjMtvH02WTc8A+HkYJ77vmxk8h2zvBMEmy6ZngHK5nJCT3PEQqrxUKslJ
qPJqtSonocpbrZachCrHPVRO5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISR
E0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZO
GFuz2RAnJznty4giVLn27+T2uM/reEluP+Dxon2jzA73Fx/XPvRIdr4Pfa1+BdSvwJzH9LXwPM91
XdzUgiD4faigNlSIUiuVSmRfi+VyaRf4H30tkL7OIjvpf5Ix1CcnEvVTYuL6buEGjfE0+26t1Z8t
HvXxi+Of+j3+AdBn5mo=
EOscribbleblack_sel

$scribbleblack_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleblack_sel))  ,'rgb',0,8,92,77,276);

#          "closed path" icon (unselected)
my $scribbleclosed= <<EOscribbleclosed;
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
EOscribbleclosed

$scribbleclosed = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleclosed))  ,'rgb',0,8,73,77,220);

#          "closed path" icon (selected)
my $scribbleclosed_sel= <<EOscribbleclosed_sel;
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
EOscribbleclosed_sel

$scribbleclosed_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleclosed_sel))  ,'rgb',0,8,73,77,220);

#          "color mode" icon (unselected)
my $scribblecolor= <<EOscribblecolor;
eJztnEtI60ocxm0VPD5AFwVXggsXPnYWQbcqLsSV4IPqRtwJLgQRQdHrQkEUhCvWFsEHXilcxGpt
ceFCXCg+Diq+EBe6sEWEVqogPqv3w3BCbprEtCbNJOm3ipP5j9/8nMxMxsx8fupCwWBwd3d3eXn5
ny/hAj8iUWlfysjn8wHCXzzCLWRQ2mPs9PHxsb6+3t/fzweEEjIgGzIr7Vd2oY5Op5NV/cHBwb+/
hAvWLWTWPJa1tTVmla1WK1L29vZ+fwkX+BGJzDxIUdq1jPJ6vfQjgwu0gd88wi1mTgQq7V0uzc3N
MR8KPiA0FjozAulC7u7uFhYWbDYbnjW73e5wOP4lVfAGh/AJt/AM5ywggUCAruPExIQwEErIRocg
HIW4XC7hnplwwT+Tyc7ODn0LXYQYJszOB/MWt9vd19cX/os4ExUXn1WPx0MzWVpaotIHBgboTlVY
yIbMVBSmczGrjtyiJ6Xz8/NUyujoqBgglJCZiqLDNSA0D4rJ7OwslYI+RzwTZKai6HANCP2kTEwS
1CCDwRD+CjM+Pq5bJunp6dvb26FQiOV8ampKn0yysrJOT09DX2I5X1xc1CGTvLy86+vr0B+xnGMM
1RuT0tJSv98fYkjnTJqamh4fH0P/l56ZDA8Ph7ikWyaYVXIC0ScTo9G4tbXFB4Q0JtXV1bm5ubIC
SU1Nvbi4EABCGhMAeX5+xht6UVGRHEBMJtPNzY0wENKYQDMzM3D1/v4uORlMQh4eHr4FQiATNJWX
lxfKG0XGbDb/HEh5eTlaoBggBDJJ+NNUaIHM5ubmT8hYLJa3tzeRQMhkkp+f//r6yvIJMnhjxa1I
gXR3dyNWPBAymUCoPqdb/LkxrygoKBBZztjYWEQ0SGbC2VSYZBwOR2FhoXAhHo8nCiDEMoFWV1eF
nXd1dfHFJiUl7e/vRweEZCYYOgU6xkAgkJGRwRmYmZnp9XqjBkIyk4SwAYipjY0NzpDs7Gzg+gkQ
wpkw5yrhGhoaYuUvLi4Of/HXGJME/gEoHEtVVZUAQC0xQa8iMADRWFpbWyOdhKiXCTQ9PQ2fPp/P
7XZzVqG3t1cqGmphgqaCcIwmuG5vb2f5b2xsRHpHR4eumLDExNLS0kKnS4hFdUwoLOg90Iew0iks
fr+/p6fn7OxMV0xMJtPKygrnrZKSkrS0NFzU1dXphwm9NDQyMiKQLTExMeqmoi4mrKUhYSwWi0Xz
TDiXhgSwGI3Gw8NDDTMRWBqqqKjgi4quV1EFE4GlIbzxUVMXThkMBvprAS0xEV4awrArHF5WVqYl
JmKWho6OjvCAoOvgKwQDUKRNhVgmES0NHR8f19fX85GJdAAik0l0S0MnJycNDQ3oQ37YVAhk8sOl
ocvLy5qamuTkZGaZEQ1ApDGRamkIZNra2mgyeKwODg7UyETapSHo6uoKZH79+oXCa2trVceE76sh
qcikpKSIbCqEMBH4akgqnZ+fu1wuVTD59quh2EtZJmK+Goq9FGQi8quh2EspJjk5OcxPl4mSIkzM
ZvPt7a3SVedV7JlUVlYGg0Gl6y0k2jO1IU5uJs3NzU9PT0pX+huxnMu6L6Ozs1P4H52EiOVcvv07
VqtV2nm7fGI5l2+fl3ol335A9Sq+bzRcEu4vVtc+dE5Jvg/9M35eQdh5BVQ51LkWdrvdZrNhUHM6
nSukCt7gEFYnJyc5z7W4v7+nKxjFuRYI/9SiJDn/RGOKn5PDqfh5SuHiO3dr9Ev6PHfrM34+G7/i
5/jxKaLzHv8DT7ueOg==
EOscribblecolor

$scribblecolor = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribblecolor))  ,'rgb',0,8,92,77,276);

#          "color mode" icon (selected)
my $scribblecolor_sel= <<EOscribblecolor_sel;
eJztnEtIK1ccxk0UfIIuAncluHDhY2cQdKsiRYRSWx9EN+LmVrDUIiIqWrndWC20ipog+MBK4CJG
Y3JduBAXirpQ8YW40IUJIiQSBfEZ7Vend0gnM+MkzmTOzORjFsmZ8x+/88uZc84c55yXF03I5/Nt
bm7Oz8///Sp8wFckyu1LHrndbkD4lUM4hQxye4ycnp+fl5eXe3p6uIBQQgZkQ2a5/UoulNFmszGK
3/5be9MfP+HAB8YpZFY9lqWlpcAi//hnY8nnb/KcBXlfXg9nAb4iMTAPQuR2LaFcLhd9y3T1dH03
+cN/KIIOnOru6aZvIgTK7V0qTU1N0b/+t5PfcwGhDmSgMyOQvsjl5eXMzIzZbB4YGLBYLFar9TOp
gjc4hE+4hWc4ZwDxer10GT/+1cgPhDo+BtxECMdF7HY7f8tMuOA/kMnGxgZ96t82RAATZKNDMG5x
OBzd3d3Bf4g1UXZxWXU6nTSTubk5Kr39U4fxS6EQJsjW8amTisJwLmLFkVr0oHR6eppK+fn3ZiFA
qKO57xcqig5XgVA9KCaTk5NUCsYhwpkgMxVFh6tAIyMjEjGJUYJ0Ol3wI8zQ0JBmmaSkpKyvr/v9
fobzsbExbTL58OHDwcGB/1UM57OzsxpkkpWVdXZ25v8qhnP0oVpjUlhY6PF4/AHSOJO6urqbmxv/
/6VlJn19fX42aZYJRpWsQLTJRK/Xr62tcQEhjUl5eXlmZqakQJKSko6Pj3mAkMYEQO7u7vCEnpeX
JwUQg8Fwfn7OD4Q0JtDExARcPT09iU4Gg5Dr6+s3gRDIBFXl/v6e8kaRMRqN7wdSXFyMGigECIFM
Yr5WFVogs7q6+h4yJpPp8fFRIBAymWRnZz88PDB8ggyeWHEqVCAdHR2IFQ6ETCYQis/qFj83xhU5
OTkCrzM4OBgSDZKZsFaVQDJWqzU3N5f/Ik6nMwwgxDKBFhcX+Z23tbVxxcbFxW1tbYUHhGQm6Dp5
Gkav15uamsoamJaW5nK5wgZCMpOYoA4oUCsrK6wh6enpwPUeIIQzCRyrBKu3t5eRPz8/P/jBX2VM
Yrg7oGAsZWVlPADVxAStCk8HRGNpbGwMdRCiXCbQ+Pg4fLrdbofDwVqErq4usWgohQmqCsLRm+Bz
c3Mzw39tbS3SW1paNMWEoUAsDQ0NdLqIWBTHhMKC1gNtCCOdwuLxeDo7Ow8PDzXFxGAwLCwssJ4q
KChITk7Gh6qqKu0woaeG+vv7ebLFxsaGXVWUxYQxNcSPxWQyqZ4J69QQDxa9Xr+zs6NiJjxTQyUl
JVxR4bUqimDCMzWEJz5q6MIqnU5Hvy2gJib8U0PodvnDi4qK1MREyNTQ7u4ubhA0HVwXQQcUalUh
lklIU0N7e3vV1dVcZELtgMhkEt7U0P7+fk1NDdqQd1YVApm8c2ro5OSkoqIiPj4+8JohdUCkMRFr
aghkmpqaaDK4rba3t5XIRNypIej09BRkEhIScPHKykrFMeF6a0gsMomJiQKrCiFMeN4aEktHR0d2
u10RTN58ayjykpeJkLeGIi8ZmQh8ayjykotJRkZG4KvLREkWJkaj8eLiQu6icyryTEpLS30+n9zl
5hPtmVoQJzWT+vr629tbuQv9hhjOJV2X0drayv+PTkLEcC7d+p3h4WFxx+3SieFcunVeypV06wGV
q+i60WCJuL5YWevQWSX6OvSX6H4FQfsVUNeh9rWwWCxmsxmdms1mWyBV8AaHsDo6Osq6r8XV1RVd
wDD2tUD4ixolyv4nKlN0nxxWRfdTChbXvlvooHFoc9+tl+j+bNyK7uPHpZD2e/wHF/Lelw==
EOscribblecolor_sel

$scribblecolor_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribblecolor_sel))  ,'rgb',0,8,92,77,276);

#          "delete point" icon (unselected)
my $scribbledelete= <<EOscribbledelete;
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
EOscribbledelete

$scribbledelete = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbledelete))  ,'rgb',0,8,92,77,276);

#          "delete point" icon (selected)
my $scribbledelete_sel= <<EOscribbledelete_sel;
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
Qo7v+L0b0ut7j/8DMo1Nzg==
EOscribbledelete_sel

$scribbledelete_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbledelete_sel))  ,'rgb',0,8,92,77,276);

#          "draw mode" icon (unselected)
my $scribbledraw= <<EOscribbledraw;
eJzt3MlL60AcB/D/1qYFURBcquITtdqDVB6oePAgVRFB3EDUuoAHcaPqwR5FbNWKSy1uWG3yvnR4
IWRrkmYyM+r3VJNJnN+HSTrdRlF+RJ6eng4ODhYXFycrwQP8iY2s+8UmV1dXQPhjEexCA9Z9DC6y
LG9vb3d3d1uBkKABmqEx6/5SD2qcn5/XlR+Lxf5Wgge6XWj87VlSqZS25JGREWw5PDw8qgQP8Cc2
attgC+teU0wul1MvGTzAGDiyCHZpW+JA1n2nlWQyqb0orEBUFrUxDmTdd5Pc398nEonGxkb0MJPJ
eDjDw8ODWuPo6Kg9CAmaqYfgcN+LqiW3t7ctLS11/xOJRE5OTtyeZH9/X3uLcGKivflg3kKjNG/R
gXhmWVhYINX19fWpN1X7oBkak6MwnaNUoNuYgnhjmZqaItXhGnQCQoLG5CgcTq9M57EB8cAyMTFB
qsM8xLkJGpOjcDjVYp0EU+umpiYbEBJJkvb29pycUHQTqxHS0NDgebQIbWI1Qvr7+19fX6enp72N
FnFNbEDe3t6UygsWbyyCmlQFIfHGIqKJQxASsGDm4IpFOBNXIMjs7KyxsT2LWCaeQUKhUDwed8gi
kEktIBsbG7iIMMN0wiKKCeYhzc3Nxop6enpeXl6qgpCN5XJ5fHzceJJwOJxOp8UyqXGEaHdhtExO
TtqPFv5NfBkh2hQKhfr6euMJo9Ho5+cn/yY+jhCSx8fHjo4OUxD1vSCeTfL5vL8jpFgsdnV1GU+I
V0wYjWozbk2YjBCeTRiC8GmSy+UYgnBowhyENxMeQLgy4QSEH5PAQNrb26t+JsWDSZAg2FW1P8xN
eANhbsIhCFsTzyAIPRCGJtyCsDLhGYSJCecgwZvwDxKwiRAgQZqIAhKYiUAgwZiIBRKASTabFQuE
tomIIFRNBAWhZyLLcmtrq7H/VT+GsAKx+hgC/+Xu7s5HEHom5+fngoIo1EyWlpYEBVGomei+GiRJ
EkozNuMQRKFjgjteKBTSljA4OGhslkql1AYrKyum5wnmpqoLDZOdnR1dFevr68Zmvb29HIIodEyG
h4d1hdzc3BibpdNpPC9vbW0ZdzEEUSiYlEol3bc7UJ2rLrEFUSiYnJ2d6WpJJBLlctlhf5iDKBRM
ZmZmjBUNDAxov+BhFR5AFAom0WjUWBSCC+r09NSmJ1Yg2BgkiOK3ST6fNwUhiUQiuLJMu8EPiOK3
CeZdNiZktFxfX+v6UCgUTCdmbW1t9CZmNvHXZGhoyN6krvK6mNxygbO2tobpXDgc5gfEX5P393dc
HVVN6iq3XPtfZjG5ZGiYHB8fOwGpGoYjxHeTZDL5DUAU/0xkWTb9LqurdHZ2MgdR/DO5vLz05iBJ
Ujwex8vAbDbLlkKNX78vXl5edkWBQYVrDbO4j48PtgLG+PU79FgsVtWB/LBodXX14uKC5+VTfFmv
4Pn5GZeAFQWeoDFv2dzc5OFe4STFYlEt0MO6FuQdxd3dXSMFbphzc3OZTKZUKrGu0nVqX/9kbGyM
OGBGilsNZviiDAmr1LhOztfXF4YEfNDA9J15QVPLekp48UJ+HvXNYrXuVqKSn7nulvK7Ppt1ftfx
s4qr9R7/AfP4FjY=
EOscribbledraw

$scribbledraw = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbledraw))  ,'rgb',0,8,92,77,276);

#          "draw mode" icon (selected)
my $scribbledraw_sel= <<EOscribbledraw_sel;
eJzt3MtPIkkcB/D/afYye5/D3jabnb9BGhJXZ0x8gA5D8MVMDM7BgwcPBDXGxPjKEBUfiQejxqAe
5GiMoGJ8IPEVUej9LjXbId100zRdXVXO/NIHoKva+n2saqqBLln+KeLm5mZ7e3t2dna0FHiAp3iR
dbvYxMnJCRA+6wR2oQDrNjoXxWJxbW0tEAjogZBAARRDYdbtpR7IcXp6WpW+t9vbOPAPNjxQ7ULh
V88Sj8fLU3YPet5N/vHm+9s3sdL2/S2e4sXyMqjCutUUI51OK0PmU+DTX5H3Pyg0G3b5A35lEKEi
67bTimg0qvz3/4z8rQdCNhRQCqMi67ZXiMvLy3A43NzcjBYmk0kLR7i6ulJylL55jEHIJpUNIlS3
Pal64vz8vK2treH/8Hg8e3t7tR5ka2tLSfC/c4gJExRTqmDeQiM1a6ECscwyMzPz410m6Pst9rsZ
ExTzBTtJLUznKCVYa1QEscYyNjZGsmv+8sEMCNk+fP1IaqE6vTTNhwGIBZZIJEKywzzEvAkKk1qo
TjVZM4GpdUtLiwEICUmSNjc3zRxQdBO9HtLU1GS5twhtotdD+vr67u/vx8fHrfUWcU0MQB4eHuTS
BYs1FkFNqoKQsMYioolJEBJg6enpqYlFOJOaQBCTk5PawsYsYplYBnG5XKFQyCSLQCb1gCwvL2MQ
YYZphkUUE8xDWltbtRkFg8G7u7uqIOTFQqEwMjKiPYjb7U4kEmKZ1NlDyneht4yOjhr3Fv5NbOkh
5ZHNZhsbG7UH9Hq9z8/P/JvY2ENIXF9fd3Z2VgRRPgvi2SSTydjbQ3K5nN/v1x4QV0zojUoxbk2Y
9BCeTRiC8GmSTqcZgnBowhyENxMeQLgy4QSEHxPHQHw+X9XvpHgwcRIEu6q2h7kJbyDMTTgEYWti
GQRBD4ShCbcgrEx4BmFiwjmI8yb8gzhsIgSIkyaigDhmIhCIMyZigThgkkqlxAKhbSIiCFUTQUHo
mRSLxfb2dm37q34NoQei9zUE/srFxYWNIPRMDg8PBQWRqZnMzc0JCiJTM1H9NEiSJKSmLcYhiEzH
BGc8l8tVnsLAwIC2WDweVwrEYrGKx3HmpKoKGibr6+uqLJaWlrTFuru7OQSR6ZgMDQ2pEjk7O9MW
SyQSeF9eXV3V7mIIIlMwyefzql93ILuamsQWRKZgcnBwoMolHA4XCgWT7WEOIlMwmZiY0GbU399f
/gMPveABRKZg4vV6tUkhMKD29/cNWqIHghedBJHtNslkMhVBSHg8Hoysis3gB0S22wTzLgMT0ltO
T09VbchmsxUnZh0dHfQmZgZhr8ng4KCxSUPpupiccoGzuLiI6Zzb7eYHxF6Tx8dHjI6qJg2lU67x
nVlMhgwNk93dXTMgVYNhD7HdJBqNvgIQ2T6TYrFY8besNUVXVxdzENk+k+PjY2sOkiSFQiFcBqZS
KbYUSth1f/H8/HxNFOhUGGuYxT09PbEV0IZd96H39vZWdSA3Fi0sLBwdHfG8fIot6xXc3t5iCOhR
4A0a85aVlRUezhVmIpfLKQlaWNeCfKK4sbGhpcAJc2pqKplM5vN51lnWHPWvfzI8PEwcMCMNh8OY
4YvSJfSiznVyXl5e0CXgs7OzU/GTeUGjnvWUcPFCbo96ZaG37hbeoLH9nOtuyb/WZ9OPX+v46UVN
6z3+C7wvVpM=
EOscribbledraw_sel

$scribbledraw_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbledraw_sel))  ,'rgb',0,8,92,77,276);

#          "move point" icon (unselected)
my $scribblemove= <<EOscribblemove;
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
6e/n+NH0XM97/B9QEX3H
EOscribblemove

$scribblemove = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribblemove))  ,'rgb',0,8,92,77,276);

#          "move point" icon (selected)
my $scribblemove_sel= <<EOscribblemove_sel;
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
EOscribblemove_sel

$scribblemove_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribblemove_sel))  ,'rgb',0,8,92,77,276);

#          "open path" icon (unselected)
my $scribbleopen= <<EOscribbleopen;
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
YoCnpyeb2xHuSzTCmTcnMfFZQUhERIRpdyZtAbGa+8olJSVsIVb9Nm2aLm6/uLo2NDR0BzEqjKEW
NjFAfvqjjk8/1cXtuY9PNxEDsKLV5KZ528DKlgQFSQkEBgrXxrC8VaTn7t593CorKzW5VVdXs4VY
jcnPPqNubvSLL2hqKi0uppbbWLm5ytz8/buNmhDoaXLTMyN+/JEq3i4rLFTm9tVX5nGR4ty5cyKB
UQMG5MTGnlu37szq1d9Nmzayf38LN81zU6t+UzuqKytT5vbDD+ZxkeLEiROxw4Y1whLK7PDjs2dj
P/kEq2SdIn/7TeElImA5sY8/pty3TwzgRkxMx88/qya3tx/huPZkG5fU1FD5IL53T0oM01KxFcxC
erpQi58fVfvRSG0t/eADmpHBFiOLlRFASSQ+fWpDzNOTqp/lmgAoYPl9wJdfKowOrFE+/FBIdXSk
usM9tIrkWqflCmpoKP39d3s010ZkpE1Trltnk9rUZOOHkVkd6mvTqipYK+G3Ixh+cXHCcq5bx6EI
9InkzhM65+zZrlQs6j//3CYVmVHk7UBRkYLdwsSrqxMuj44bp5CqfunMnDNh0/D998r+BqwwdhST
du5UE8a7h/c3Yc8eXTGt8CBsejtQWqqbm/rvY96wfsOk8vLSQQyZ1SMv3Ue13Y6kJB3cmCeyW/82
nXkBk/j++1zEkI35a9c3bEyKOHOGOjtrEEOGn3563YoaA+ip7JEKD5b8yPAWAwFHSorguCV+/Ouv
FQJ6JWhc93r9QKyMgBgLOTz4omdh9cZz+weK+B9VPPuk
EOscribbleopen

$scribbleopen = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleopen))  ,'rgb',0,8,73,77,220);

#          "open path" icon (selected)
my $scribbleopen_sel= <<EOscribbleopen_sel;
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
EOscribbleopen_sel

$scribbleopen_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleopen_sel))  ,'rgb',0,8,73,77,220);

#          "select path mode" icon (unselected)
my $scribbleselectpath= <<EOscribbleselectpath;
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
EOscribbleselectpath

$scribbleselectpath = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleselectpath))  ,'rgb',0,8,92,77,276);

#          "select path mode" icon (selected)
my $scribbleselectpath_sel= <<EOscribbleselectpath_sel;
eJzVnH9MT98fx5Vf+VWiqKF9KkKiopXW1yj6NY0iIosiKklflaUUb+kHImIk0TJfS1lD+bS2mtZm
izZ/mF9tGJtszY+NYfO77/P7Pn1eu99739173u96395ee89y3+ece87jnvP6dc779vSoIV1dXW1t
bVe10tjYePv27S9fvqhy51758OFDR0fHjRs3/qMV/IH/4qKafYAAQkFBgUZJDh48WF5e/uzZMyN1
4/Xr14DQ193xFQoY6dZCOXfunCIKkezfvx//Hjhw4Pjx45hUA9KN379/t7a2ok35W6MAiqHwgNxU
Kg0NDaI7JicnR0RE+Pr6enp6ztEK/vDx8QkODo6Kitq+fTujIZXKysr+9ARjvHbtmqjN7PzslGM7
8cEfoq9QeMCxQD8IV0pWVlZoaOikSZOGKMnIkSOdnZ0XL168YcOGzMxMUVfPnDljWH+am5uF7SSd
2L6sNmT+3wvnN2o/fy/Ef3FRWAZVBhCIsAO5ubkhISGjR49WpCGVoUOHzpgxA/MqJydH2NvOzk69
+oPVR0tm34F9ERcje1FIPvhq/4H9tIgGatlWVFRQ5xMSEmxtbQ2gIZIxY8b4+/tjslHLMFX8Xbp0
6RJVXHlxdV9A2AcFqDAq9h9IUVERaw1qISgoCA+6/0BILC0t165dqy+W9+/fU5XE0u3yQNgnUbCI
UN1gGt+/f8/Ly2PtZGdnu7q6DiANoSxZsoQ6/PbtW8WO3b17l8r/T4dwMEExqgK/xWAgtGDT0tIm
T55sJCBMli5dyu4FZ0axb9evX+99Ugf3Lmj05WGCYnsP9mowuHOGASGqKSkp48ePNyoQiJmZWXx8
PLtjS0uLfPcuX77MSv77yC4eIOyzqziN1UJ1A5jgYbHq8C7Gjh1rbCBM7Ozs9u3bx6yDfPcuXrzY
+7yO7eRngsKsFqrrC+TIkSM0Q8aNG6cOECZwYNit5eMUlZnQ7dLT062srNQEAnFzc2N3LysrMxEm
3d3drBYcqmnTpqkMZIjW42WBgLymVZMJqRFvb28DRmRtbe3k5OTg4GBjYzNs2DDDsECDsT6YAhP4
S6wK9D+sgF4DgVMK10sU68GCR0dHw/dwcXHhV9QIG02HCU0Se3t7vYBglWH4GiWJjY3laW3lypUm
wgR6npWPi4vTC4inp6cwmisvL0dwVFJSkp+fz67Q5IGdHT58uGKDkZGRJsKksrKSlZ87dy4nDXNz
89DQUKJRXFwsbRbRbmFhIfnDc+bMUWx227ZtJsIEPWfPlDMDABVKvoSmD8/w6NGjouWTm5vr7u4u
0+zEiRNNx+703iIlhQcINPD69etppDqD2WPHjulMr+HivHnz+mo5IiKCFWtrazMRJuvWreNh4uPj
Q2PUmaKhPkOuXLnyTCv4g13JysoaNWqUtNmAgACqJd9bNZlA5/MwSU1NlQGCR0xDQwD7SyA1NTXs
OqJgag3LEMZ6y5YtVOvevXumwyQ4OFgRiIWFBStcUFAgbefp06c0NOhtxNdCJsJvMzMzYZ0TExOF
qTZIe3u7Ym/VZLJ8+XJFJra2tqxwaWmpqBFhhuHEiROfPn369f+CFaTpW/Ly8jiTpWoyWbVqlSKT
v/76i0Zx9uxZ4WYfJeWKiooQOv2SSG1tLSsg2pGBP4MpxNNP9Zls3LhRkQl8DOkjxpyhDAPIYD5I
gQj1TD/3BNVhwh7crl27FJlAnJ2dV69evXfvXp1L4M6dO1IgDx48oAIw0/0BohoT5orDeUC0zoNl
iDau9/DwgPkWwrl586YUyKtXr8jV50m3mggTxCmsPMwiJxMmMEPw9FjdqqqqHz9+iIAgksLEIDUC
PfynMKFsUkhICD8QhDwxMTGs4qlTp6BvRUC+fv1KtNks6j8Q1Zj0/KNmMzIy+He1KAY8dOjQmzdv
REB+/vxJThoT5u03Njb+KUxohnPubXl5ebHyioYGoV9cXBzLyVOV/uzbqsbk3bt3rEpycrLiVHFy
csJIWXl5Q4O5wSBbWVkFBgZSLQ2HDz/oTHoEW8N+fn4yQBDR05EJRUPj7+8vqgsviLDIx7+mwARK
ktXCPJ85c6ZOIDA0O3bsYMUUDU1kZKS0BWjmsLAwwvLy5UtTZgKpq6tjFeF1zJo1SzocfkOzdetW
mWQjDBxh0ddAq8yks7OTwhaoAkSFwl0JfkOTlpYmv4doZmZGpyxwR5NlIs0WQnbv3s3yqPyGBnOM
J/k/YsSIpKQkVkUvh19NW9xXthD/pqamkjHlNDQ8Ym1tTeq6vr7epJgIMxvSbKFQ9DU0ioKIkmhz
HvFVhwlF+rW1tcLBihxRwwyNouh1IEc1JpTkESkK4fxRNDRYXzY2NgYwgYuYmJjIGrl//76JMCFb
A29BOGRybjkjGgi8Fywffc9pODo68k8VNfMnkMePH4umgYYvdSYSqIiAgAC9DkmSf4sHYQpMMA1Y
+Y6ODtHACwsLFQ1NaWkpllV1dTXbTySJj4/XuZWjU1xcXFit06dPmwITUpK3bt0SjV165ZdS6oyc
YY32RBznfiuc3uzsbA2HC6cCE6Gr1tDQIFUaoitCQwN5+PChtE2UIb0dGxvLuYiio6NZlUFkQkcs
SDD/pbNCpGGEqTMmoCptXLjdI9z4k5GgoCBWXj4CMh4Tsikabcae/XHhwgUZIDoNjUarUkpKSmSY
Q+Xa2dkpMqHwQT61YjwmNLc3b94MTcjS79CWMkyePHnS3Nzc3t4OL+L58+ciX1fnrk1TUxP7Njw8
XJGJh4cHKyx/8N5ITOgoMoAgFkN/2FSB4ZBfO1KhmaNzBV29epVFTDzZb09PT9aU/K6xkZiwb7Oy
sujcOJ0W+Pbtm15MaGdcev6ZVEpubi7CvT+CyZo1a6g/xARaVC8m5P9LmZC9DgwMVAQCWbhwISv/
6NEjlZng8bH5LDQHycnJrIo0qJGXvtYOnZGDi8J5XJaSbzJAjMSE8q5CJuQbwB9T5PD58+fu7u6+
dCzahxliF6G6eX4zyISOhKnPpOeftRMTE0P98fPzYxfhyX/8+BHjwsChK1pbW+vr66GT8dxhlWg5
CAWzDtcRIFAsyQQm2M3NjRMI5tKePXt0rkF1mLDO5+TkWFhYsC65urpKB9sfycjIkGa5ZcTd3Z1V
lJ72UYcJfDNWYMGCBaxLDg4O/ecA+5KQkLBixYrZs2frdeQezv/Onb19Vsy2GYkJWcmkpCTWqwkT
JmCqp6enJyYm4iL+hesCwwT7CFzQCfDrzM3Np0+f7uvr+y+teHt7w8vCBHNycrK3t+/Pr58o1Xb4
8GF5IMZjAqEfUOOZDtFuLjDnTX2ZOnUqpWR53vxgPCZdXV00VTABBoXGEG2KgE6wcB7GMGpcTBvE
WAiDxYTOTus8XKo+E3JU4EVAn6gPhBwAjT47pMbOKVVXV9MKIrusjri4uNAuG0+6XjUmPYJfM23a
tGlgf3ovI7BTdIK6rq6OH0iPKr8vFibEoqKi+I8+GixTpkxhW6Isv60XkB61focuTELCd0KfjQdk
/vz5LBcNIFDy+gLpUfF9BWSaNVp3dNmyZfzbEJwC1PRLKADhcc90CsIx6qoB77VAdb1uRxvHGu1P
JxYtWtR/MpaWlpgbUFYagZw/f94wIExUfv8JrVYmMNPh4eF6rSa4YSjv5eWFwIdOmJAg/Hzx4kV/
gPQM0ntyysrKRGOJi4tzdHQUGiaM3cbGBhcR0mJGhYWFYTLQFoBU8vPz5RNoeslgvU+pqqpKNC6o
mlStSN8WJYOipqZmQE6VC6Wv927BQONj7PduwaHSmUrSKZifKHzy5MmWlpYB5yCSQX8/W2dnJ3wJ
yqThRnD2iouLKyoqmpqaFA8DGE9M5D1+Jih6ve/xv7A6i88=
EOscribbleselectpath_sel

$scribbleselectpath_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribbleselectpath_sel))  ,'rgb',0,8,92,77,276);

#          "white mode" icon (unselected)
my $scribblewhite= <<EOscribblewhite;
eJztnE2LglAYhX9606K2wkClBEE0EQyR1dSqRes+fkYti/oB5Ry8cBGPRjNkpp1nZdf32rkPaW7u
GwRvwel0Wq/Xk8nkKwQH+IjBvHPlw36/h4SPFHAKBXlnfB7X63W5XFar1TQhBhSgDMV5580crNH3
/djy6/X6ZwgOYqdQXHoti8UiuuRms4mRzWazDcEBPmIwWoORvFNnyG63s7cMDvAb2KaAU9FKTMw7
e1b0er3oTZEmxGqxxZhoL3I8HofDoeu6uNc8zxsMBt+vCrIhIXIiLTIjeUzI4XCwa2y1WreFGFBm
p2A6LjKdTm8/mV8c5I86Wa1W9hQeEfc4iT588N4ym80qlQp/UeJg7qRFnc/n1sl4PDbjtVrNPlRv
gzIUm1l4nXvacrLGvpT2+30z4jjOPUIMKDaz7PQSgJ+HcdLtds0Injn3O0GxmWWnlwA8JzNycikO
seSNRkNOYsk7nY6cxJKPRiM5iSXHf6icyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4yc
MHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLCyAkjJ4ycMHLC
yAkjJ4ycMDaz2RAnJxfty0gillz7dy5P3OdVXLLbD1hctG+UeeD+4mLtQ0/k4fvQA/UroH4F5jqm
r4Xnea7r4k/N9/2fVwXZkBBR2+12Yl+L8/lsF/iPvhaYHpSRh/Q/KRnqk5OI+ikxaX23nJD37LsV
qD9bOurjl8af+j3+AiVSUtg=
EOscribblewhite

$scribblewhite = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribblewhite))  ,'rgb',0,8,92,77,276);

#          "white mode" icon (selected)
my $scribblewhite_sel= <<EOscribblewhite_sel;
eJztnMGK2lAUht9pupnuu+iuDO1DTAdaOl06ZWyYrloKrSAmCEKwIgxi1OpsXLjW59Clog+g9u/c
4SL5k8EWYzTzf9yF3pwTz/00Jpt71usnwXw+H41G7Xb71z14gbeYTLuudJhMJpDwOQYcQkDaNe6P
1Wo1GAwcx4kTYkAAwhCcdr2JgzUGQRBafu5L7t339xh4ETqE4Mxr6ff7m0t+++Pixe3Lk97pyd39
6J3iLSY3Y5CSdtUJMh6P7SVz7Vyf+W8eVNDAobyTtxcREtOuPSmq1ar99l/5r+OEmIEAG4xEe5LZ
bNZoNFzXLRQKnufV6/XbQwW1oULUiWpRMyoPCZlOp3aN5z8vHhdixvnGRYR0nKTT6Tz+z3zgoP5N
J8Ph0B76+x+yhROE2RQ8t3S73Xw+zx8UOZk6caX2ej3rpNVqmfnczdWzu+fbOEHY1c0nk4XHub0t
J2nsQ2mtVjMzH75ebiPEjMtvH02WTc8A+HkYJ77vmxk8h2zvBMEmy6ZngFKplJCT5fEQqrxYLMpJ
qPJKpSInocqbzaachCrHPVRO5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISR
E0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZOGDlh5ISRE0ZO
GFuz2RAnJ0vty4giVLn27yz3uM/reEluP+Dxon2jzA73Fx/XPvRIdr4Pfa1+BdSvwJzH9LXwPM91
XdzUgiD4faigNlSIUsvlcmRfi8ViYRf4H30tkL7OIjvpf5Ix1CcnEvVTYuL6buEGjfE0+26t1Z8t
HvXxi+Of+j3+Ae16kzU=
EOscribblewhite_sel

$scribblewhite_sel = Gtk3::Gdk::Pixbuf->new_from_data (uncompress(decode_base64($scribblewhite_sel))  ,'rgb',0,8,92,77,276);

return($scribbleadd,$scribbleadd_sel,$scribbleblack,$scribbleblack_sel,$scribbleclosed,$scribbleclosed_sel,$scribblecolor,$scribblecolor_sel,$scribbledelete,$scribbledelete_sel,$scribbledraw,$scribbledraw_sel,$scribblemove,$scribblemove_sel,$scribbleopen,$scribbleopen_sel,$scribbleselectpath,$scribbleselectpath_sel,$scribblewhite,$scribblewhite_sel);
}
#
#     end initicons sub
#
#----------------------------------------------------------------




