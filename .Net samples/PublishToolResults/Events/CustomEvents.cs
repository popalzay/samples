using ArcGIS.Core.Events;
using ArcGIS.Desktop.Framework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PublishToolResults.Events
{
    public class CustomEvents<T>: CompositePresentationEvent<T>
    {
        /// <summary>
        /// Allow subscribers to register for our custom event
        /// </summary>
        /// <param name="action">The callback which will be used to notify the subscriber</param>
        /// <param name="keepSubscriberReferenceAlive">Set to true to retain a strong reference</param>
        /// <returns><see cref="ArcGIS.Core.Events.SubscriptionToken"/></returns>
        public static SubscriptionToken Subscribe(Action<T> action, bool keepSubscriberReferenceAlive = false)
        {
            return FrameworkApplication.EventAggregator.GetEvent<CustomEvents<T>>()
                .Register(action, keepSubscriberReferenceAlive);
        }

        /// <summary>
        /// Allow subscribers to unregister from our custom event
        /// </summary>
        /// <param name="subscriber">The action that will be unsubscribed</param>
        public static void Unsubscribe(Action<T> subscriber)
        {
            FrameworkApplication.EventAggregator.GetEvent<CustomEvents<T>>().Unregister(subscriber);
        }
        /// <summary>
        /// Allow subscribers to unregister from our custom event
        /// </summary>
        /// <param name="token">The token that will be used to find the subscriber to unsubscribe</param>
        public static void Unsubscribe(SubscriptionToken token)
        {
            FrameworkApplication.EventAggregator.GetEvent<CustomEvents<T>>().Unregister(token);
        }

        /// <summary>
        /// Event owner calls publish to raise the event and notify subscribers
        /// </summary>
        /// <param name="payload">The associated event information</param>
        internal static void Publish(T payload)
        {
            FrameworkApplication.EventAggregator.GetEvent<CustomEvents<T>>().Broadcast(payload);
        }
    }
}
