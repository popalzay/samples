using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PublishToolResults.Events
{
    /// <summary>
    /// Inherits from EventArgs  
    /// </summary>
    public class FeaturesSelectedEventArgs:EventArgs
    {
        /// <summary>
        /// Place holder for Total selected Features
        /// </summary>
        public long TotalSelectedFeatures { get; set; }
        public FeaturesSelectedEventArgs(long totalSelectedFeatures)
        {
            TotalSelectedFeatures = totalSelectedFeatures;
        }
    }
}
