using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using System.Windows.Input;
using PublishToolResults.Events;

namespace PublishToolResults
{
    internal class MainDockpaneViewModel : DockPane
    {
        private const string _dockPaneID = "PublishToolResults_MainDockpane";
        
        //copy SelectMapTool ID from Config file tool section, normally it is add-in namespace plus underscore and the maptool name
        private const string _selectionSegmentToolID = "PublishToolResults_SelectMapTool";
        protected MainDockpaneViewModel()
        {
            //Subscribe to segment selection tool complete event
            CustomEvents<FeaturesSelectedEventArgs>.Subscribe((args) => TotalFeatures = args.TotalSelectedFeatures);
        }


        /// <summary>
        /// This property is bound to UI textbox
        /// </summary>
        private long _totalFeatures;
        public long TotalFeatures
        {
            get
            {
                return _totalFeatures;
            }
            set
            {
                SetProperty(ref _totalFeatures, value);
            }
        }

        public ICommand SelectFeatureCommand
        {
            get
            {
                return FrameworkApplication.GetPlugInWrapper(_selectionSegmentToolID) as ICommand;
            }

        }
        /// <summary>
        /// Show the DockPane.
        /// </summary>
        internal static void Show()
        {
            DockPane pane = FrameworkApplication.DockPaneManager.Find(_dockPaneID);
            if (pane == null)
                return;

            pane.Activate();
        }


    }

    /// <summary>
    /// Button implementation to show the DockPane.
    /// </summary>
    internal class MainDockpane_ShowButton : Button
    {
        protected override void OnClick()
        {
            MainDockpaneViewModel.Show();
        }
    }
}
