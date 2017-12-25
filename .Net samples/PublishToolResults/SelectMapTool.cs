using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Mapping;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using PublishToolResults.Events;

namespace PublishToolResults
{
    internal class SelectMapTool : MapTool
    {
        public SelectMapTool()
        {
            IsSketchTool = true;
            SketchType = SketchGeometryType.Rectangle;
            SketchOutputMode = SketchOutputMode.Map;
        }

        protected override Task OnToolActivateAsync(bool active)
        {
            return base.OnToolActivateAsync(active);
        }

        protected override async Task<bool> OnSketchCompleteAsync(Geometry geometry)
        {
            if (geometry == null)
                return true;
            var result = await QueuedTask.Run(() =>
            {
                string LayerName = "YOUR LAYER NAME";

                //Count of feature selected features
                long featureCount = MapView.Active.GetFeatures(geometry).FirstOrDefault(fl => fl.Key.Name == LayerName).Value.Count;

                //change the selection tool to esri mapping explore after selection
                FrameworkApplication.SetCurrentToolAsync(DAML.Tool.esri_mapping_exploreTool);

                return featureCount;
            });

            //Publishes the result 
            CustomEvents<FeaturesSelectedEventArgs>.Publish(new FeaturesSelectedEventArgs(result));

            return true;
        }
    }
}
