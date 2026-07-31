import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ArrowLeft, FileText, Sparkles, MapPin, Navigation, 
  Upload, CheckCircle2, AlertCircle, Phone 
} from 'lucide-react';
import './LodgeComplaint.css';

export const LodgeComplaint = () => {
  const { apiFetch } = useAuth();
  const navigate = useNavigate();
  
  // Form States
  const [departments, setDepartments] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [departmentId, setDepartmentId] = useState('');
  const [contactNumber, setContactNumber] = useState('');
  const [address, setAddress] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [pincode, setPincode] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  
  // Image upload
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  
  // Status states
  const [loading, setLoading] = useState(false);
  const [detectingLoc, setDetectingLoc] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Fetch departments dropdown list
  useEffect(() => {
    const fetchDepts = async () => {
      try {
        const response = await apiFetch('/api/departments/');
        if (response.ok) {
          const data = await response.json();
          setDepartments(data.departments || []);
        }
      } catch (err) {
        console.error('Error fetching departments:', err);
      }
    };
    fetchDepts();
  }, []);

  // GPS geolocation handler
  const handleGPSDetect = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      return;
    }

    setDetectingLoc(true);
    setError('');
    
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        setLatitude(lat.toString());
        setLongitude(lng.toString());
        
        // Reverse Geocode via backend proxy
        try {
          const response = await apiFetch(`/api/geocode/reverse/?lat=${lat}&lon=${lng}`);
          if (response.ok) {
            const data = await response.json();
            const addr = data.address || {};
            
            // Build nice address
            const street = addr.road || addr.suburb || addr.neighbourhood || '';
            const block = addr.residential || addr.state_district || '';
            const finalAddr = data.display_name || `${street} ${block}`.trim();
            
            setAddress(finalAddr);
            setCity(addr.city || addr.town || addr.village || addr.city_district || '');
            setState(addr.state || '');
            setPincode(addr.postcode || '');
            setSuccess('Location coordinates and address detected successfully!');
          } else {
            setSuccess('GPS coordinates captured, but reverse address lookup failed.');
          }
        } catch (err) {
          console.error(err);
          setSuccess('GPS coordinates captured, but address resolution skipped due to connection.');
        } finally {
          setDetectingLoc(false);
        }
      },
      (err) => {
        console.error('GPS error:', err);
        setError('Failed to capture GPS. Please ensure location permissions are granted.');
        setDetectingLoc(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      // Clean up previous preview URL to prevent memory leaks
      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }
      // Create local preview URL
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleRemoveImage = () => {
    setImageFile(null);
    if (imagePreview) {
      URL.revokeObjectURL(imagePreview);
      setImagePreview(null);
    }
  };

  // Cleanup object URL on unmount
  useEffect(() => {
    return () => {
      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }
    };
  }, [imagePreview]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!title || !description) {
      setError('Grievance title and detailed description are required.');
      return;
    }

    setLoading(true);

    // Create FormData since we are sending files
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('contact_number', contactNumber);
    formData.append('address', address);
    formData.append('city', city);
    formData.append('state', state);
    formData.append('pincode', pincode);
    if (latitude) formData.append('latitude', latitude);
    if (longitude) formData.append('longitude', longitude);
    
    if (departmentId) {
      formData.append('department', departmentId);
    }
    if (imageFile) {
      formData.append('image', imageFile);
    }

    try {
      const response = await apiFetch('/api/complaints/create/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok && data.success) {
        setSuccess(`Grievance #${data.id} registered successfully! Categorized under '${data.department}' with '${data.urgency}' urgency.`);
        setTimeout(() => {
          navigate('/dashboard');
        }, 3000);
      } else {
        setError(data.error || 'Failed to lodge complaint. Please check fields.');
        setLoading(false);
      }
    } catch (err) {
      console.error(err);
      setError('Network error lodging grievance.');
      setLoading(false);
    }
  };

  return (
    <div className="lodge-complaint-wrapper">
      <div className="lodge-container">
        {/* Back Link */}
        <div className="back-link-wrap">
          <Link to="/dashboard" className="btn-back">
            <ArrowLeft size={16} />
            Back to Dashboard
          </Link>
        </div>

        {/* Header */}
        <div className="lodge-header-card card-box">
          <div className="badge-spark">
            <Sparkles size={16} />
            AI Assisted Automatic Dispatch Prototype
          </div>
          <h2>Lodge a Grievance</h2>
          <p>
            Submit details below. The project prototype will analyze the text to prioritize and dispatch your complaint to the correct officer automatically.
          </p>
        </div>

        {/* Notifications */}
        {error && (
          <div className="alert-badge error">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}
        {success && (
          <div className="alert-badge success">
            <CheckCircle2 size={20} />
            <span>{success}</span>
          </div>
        )}

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="lodge-form">
          <div className="form-sections-grid">
            
            {/* Left Column: Complaint Details */}
            <div className="form-column card-box">
              <h3 className="column-title">
                <FileText size={18} className="column-title-icon" />
                Grievance Description
              </h3>

              <div className="form-group-lodge">
                <label className="form-label-lodge" htmlFor="complaint-title">Grievance Title *</label>
                <input
                  id="complaint-title"
                  type="text"
                  className="form-input-lodge"
                  placeholder="e.g. Broken streetlight on 4th cross road"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  disabled={loading}
                />
              </div>

              <div className="form-group-lodge">
                <label className="form-label-lodge" htmlFor="complaint-desc">Detailed Explanation *</label>
                <textarea
                  id="complaint-desc"
                  rows={6}
                  className="form-textarea-lodge"
                  placeholder="Provide maximum details like exact landmarks, how long the issue has persisted, or damage details. This description will be parsed by NLTK AI to auto-route the department."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  disabled={loading}
                />
              </div>

              <div className="form-group-lodge">
                <label className="form-label-lodge" htmlFor="complaint-dept">Target Department (Optional)</label>
                <select
                  id="complaint-dept"
                  className="form-select-lodge"
                  value={departmentId}
                  onChange={(e) => setDepartmentId(e.target.value)}
                  disabled={loading}
                >
                  <option value="">Auto-Detect via AI Engine (Recommended)</option>
                  {departments.map(d => (
                    <option key={d.id} value={d.id}>{d.name} (SLA: {d.slaHours} hours)</option>
                  ))}
                </select>
                <small className="help-text">
                  Leaving this as "Auto-Detect" will leverage our NLP categorizer to route the request to the matching department.
                </small>
              </div>

              <div className="form-group-lodge">
                <label className="form-label-lodge" htmlFor="complaint-contact">Contact Number</label>
                <div className="input-with-icon-lodge">
                  <Phone size={16} className="lodge-inside-icon" />
                  <input
                    id="complaint-contact"
                    type="text"
                    className="form-input-lodge with-icon"
                    placeholder="Enter phone number"
                    value={contactNumber}
                    onChange={(e) => setContactNumber(e.target.value)}
                    disabled={loading}
                  />
                </div>
              </div>
            </div>

            {/* Right Column: Location & Attachments */}
            <div className="form-column flex-column-gap">
              {/* Location Card */}
              <div className="column-card card-box">
                <div className="title-between-flex">
                  <h3 className="column-title m-0">
                    <MapPin size={18} className="column-title-icon" />
                    Geographical Details
                  </h3>
                  <button
                    type="button"
                    onClick={handleGPSDetect}
                    className="btn-detect-gps"
                    disabled={loading || detectingLoc}
                  >
                    <Navigation size={14} className={detectingLoc ? 'spin-icon' : ''} />
                    {detectingLoc ? 'Detecting...' : 'Detect GPS Address'}
                  </button>
                </div>

                <div className="form-group-lodge">
                  <label className="form-label-lodge" htmlFor="complaint-address">Street Address / Landmark</label>
                  <textarea
                    id="complaint-address"
                    rows={2}
                    className="form-textarea-lodge"
                    placeholder="Enter address details"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    disabled={loading}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  <div className="form-group-lodge">
                    <label className="form-label-lodge" htmlFor="complaint-city">City</label>
                    <input
                      id="complaint-city"
                      type="text"
                      className="form-input-lodge"
                      placeholder="City"
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group-lodge">
                    <label className="form-label-lodge" htmlFor="complaint-state">State</label>
                    <input
                      id="complaint-state"
                      type="text"
                      className="form-input-lodge"
                      placeholder="State"
                      value={state}
                      onChange={(e) => setState(e.target.value)}
                      disabled={loading}
                    />
                  </div>
                </div>

                <div className="form-group-lodge">
                  <label className="form-label-lodge" htmlFor="complaint-pincode">Pincode</label>
                  <input
                    id="complaint-pincode"
                    type="text"
                    className="form-input-lodge"
                    placeholder="Pincode"
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value)}
                    disabled={loading}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  <div className="form-group-lodge">
                    <label className="form-label-lodge">Latitude</label>
                    <input
                      type="text"
                      className="form-input-lodge disabled"
                      placeholder="Detect via GPS"
                      value={latitude}
                      disabled
                    />
                  </div>
                  <div className="form-group-lodge">
                    <label className="form-label-lodge">Longitude</label>
                    <input
                      type="text"
                      className="form-input-lodge disabled"
                      placeholder="Detect via GPS"
                      value={longitude}
                      disabled
                    />
                  </div>
                </div>
              </div>

              {/* Photo Upload Card */}
              <div className="column-card card-box">
                <h3 className="column-title">
                  <Upload size={18} className="column-title-icon" />
                  Site Visit Photo Attachments
                </h3>
                
                <div className="file-uploader-box">
                  <input
                    type="file"
                    id="complaint-photo"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden-file-input"
                    disabled={loading}
                  />
                  
                  {imagePreview ? (
                    <div className="preview-image-wrap">
                      <img src={imagePreview} alt="Lodge complaint preview" className="lodge-img-preview" />
                      <button 
                        type="button" 
                        onClick={handleRemoveImage} 
                        className="btn-remove-preview"
                      >
                        Remove Photo
                      </button>
                    </div>
                  ) : (
                    <label htmlFor="complaint-photo" className="upload-dropzone">
                      <Upload size={32} className="dropzone-upload-icon" />
                      <span className="dropzone-text">Click to browse image files</span>
                      <span className="dropzone-sub">Supported formats: JPG, PNG, GIF</span>
                    </label>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Form Actions */}
          <div className="form-actions-bar card-box">
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="btn-cancel-lodge"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-submit-lodge"
              disabled={loading}
            >
              {loading ? 'Submitting Grievance...' : 'Submit Grievance to Portal'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LodgeComplaint;
