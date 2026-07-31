import React, { useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import { Link } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';

const URGENCY_COLORS = {
  critical: '#ef4444',
  high: '#f97316',
  medium: '#eab308',
  low: '#3b82f6',
};

const DEFAULT_CENTER = [20.5937, 78.9629];
const DEFAULT_ZOOM = 5;

/**
 * DashboardMap — declarative react-leaflet implementation.
 *
 * Key improvements over the old Leaflet imperative version:
 * - No window.navigateToComplaint global pollution
 * - No direct DOM manipulation
 * - Uses react-router <Link> inside popups via React Portal pattern
 * - Proper lifecycle managed by react-leaflet
 * - Accessible: aria-label on container, keyboard-focusable popup links
 */
export const DashboardMap = ({ complaints = [] }) => {
  const geolocated = useMemo(
    () => complaints.filter(c => c.latitude && c.longitude),
    [complaints]
  );

  // Compute initial bounds from complaints so map auto-fits on load
  const center = useMemo(() => {
    if (geolocated.length === 0) return DEFAULT_CENTER;
    const avgLat = geolocated.reduce((s, c) => s + Number(c.latitude), 0) / geolocated.length;
    const avgLng = geolocated.reduce((s, c) => s + Number(c.longitude), 0) / geolocated.length;
    return [avgLat, avgLng];
  }, [geolocated]);

  const zoom = geolocated.length > 0 ? 7 : DEFAULT_ZOOM;

  return (
    <div
      aria-label="Grievance locations map"
      role="region"
      style={{
        height: '100%',
        width: '100%',
        borderRadius: 'var(--radius-md)',
        overflow: 'hidden',
        border: '1px solid var(--border-color)',
      }}
    >
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={false}
        aria-label="India grievance map"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          maxZoom={19}
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {geolocated.map(complaint => {
          const color = URGENCY_COLORS[complaint.urgency] || URGENCY_COLORS.low;

          return (
            <CircleMarker
              key={complaint.id}
              center={[Number(complaint.latitude), Number(complaint.longitude)]}
              radius={8}
              pathOptions={{
                fillColor: color,
                color: '#ffffff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.85,
              }}
            >
              <Popup>
                <div style={{ fontFamily: 'var(--font-sans)', minWidth: 170, padding: '2px 0' }}>
                  <p style={{ margin: '0 0 2px', fontWeight: 700, color: 'var(--primary-blue)', fontSize: '0.82rem' }}>
                    Grievance #{complaint.id}
                  </p>
                  <p style={{ margin: '0 0 4px', fontWeight: 600, color: 'var(--text-dark)', fontSize: '0.8rem', lineHeight: 1.3 }}>
                    {complaint.title}
                  </p>
                  <p style={{ margin: '0 0 6px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    {complaint.city || 'Unknown'}{complaint.state ? `, ${complaint.state}` : ''}
                  </p>
                  <div style={{ display: 'flex', gap: 4, marginBottom: 8 }}>
                    <span style={{
                      backgroundColor: color, color: '#fff', fontSize: '0.6rem',
                      padding: '2px 7px', borderRadius: 99, fontWeight: 700, textTransform: 'uppercase',
                    }}>
                      {complaint.urgency}
                    </span>
                    <span style={{
                      backgroundColor: 'var(--text-muted)', color: '#fff', fontSize: '0.6rem',
                      padding: '2px 7px', borderRadius: 99, fontWeight: 700, textTransform: 'uppercase',
                    }}>
                      {(complaint.status || '').replace('_', ' ')}
                    </span>
                  </div>
                  {/* React-router Link — no window pollution */}
                  <Link
                    to={`/complaints/${complaint.id}`}
                    style={{
                      display: 'block',
                      textAlign: 'center',
                      backgroundColor: 'var(--primary-blue)',
                      color: '#fff',
                      borderRadius: 4,
                      padding: '4px 8px',
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      textDecoration: 'none',
                    }}
                    aria-label={`View details for grievance ${complaint.id}`}
                  >
                    View Details →
                  </Link>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>

      {geolocated.length === 0 && (
        <div style={{
          position: 'absolute', inset: 0, display: 'flex',
          alignItems: 'center', justifyContent: 'center',
          pointerEvents: 'none', color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)',
        }}>
          No geolocated grievances to display
        </div>
      )}
    </div>
  );
};

export default DashboardMap;
