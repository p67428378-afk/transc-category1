import React, { useState } from 'react';

function UploadForm({ onUploadSuccess, apiBaseUrl }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    setUploading(true);
    setMessage('Uploading...');
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);
    // You might want to add a user_id here if your backend requires it
    // formData.append('user_id', 'some_user_id');

    try {
      const response = await fetch(`${apiBaseUrl}/transactions/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || 'Upload successful!');
        onUploadSuccess(); // Notify parent component to refresh data
        setSelectedFile(null); // Clear selected file
      } else {
        setError(data.error || 'Upload failed.');
      }
    } catch (e) {
      console.error("Error during upload:", e);
      setError('Network error or server unreachable.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-form">
      <input type="file" accept=".csv" onChange={handleFileChange} disabled={uploading} />
      <button onClick={handleUpload} disabled={!selectedFile || uploading}>
        {uploading ? 'Uploading...' : 'Upload CSV'}
      </button>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default UploadForm;
