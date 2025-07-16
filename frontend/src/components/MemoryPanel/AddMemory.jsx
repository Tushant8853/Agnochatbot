import React, { useState } from 'react';
import './AddMemory.css';

const AddMemory = ({ onAddMemory }) => {
  const [content, setContent] = useState('');
  const [memoryType, setMemoryType] = useState('fact');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    setMessage('');

    try {
      await onAddMemory(content.trim(), memoryType);
      setContent('');
      setMessage('Memory added successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to add memory. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-memory">
      <h4>Add New Memory</h4>
      <p className="add-memory-description">
        Add a new fact or memory to your AI assistant's knowledge base.
      </p>

      <form onSubmit={handleSubmit} className="add-memory-form">
        <div className="form-group">
          <label htmlFor="memory-content">Memory Content</label>
          <textarea
            id="memory-content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter the memory or fact you want to add..."
            className="memory-textarea"
            rows="4"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="memory-type">Memory Type</label>
          <select
            id="memory-type"
            value={memoryType}
            onChange={(e) => setMemoryType(e.target.value)}
            className="memory-type-select"
            disabled={loading}
          >
            <option value="fact">Fact</option>
            <option value="preference">Preference</option>
            <option value="experience">Experience</option>
            <option value="custom">Custom</option>
          </select>
        </div>

        {message && (
          <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        <button 
          type="submit" 
          className="add-memory-button"
          disabled={!content.trim() || loading}
        >
          {loading ? 'Adding...' : 'Add Memory'}
        </button>
      </form>

      <div className="memory-examples">
        <h5>Examples</h5>
        <div className="example-list">
          <div className="example-item">
            <strong>Fact:</strong> "I work as a software engineer at Tech Corp"
          </div>
          <div className="example-item">
            <strong>Preference:</strong> "I prefer dark mode interfaces"
          </div>
          <div className="example-item">
            <strong>Experience:</strong> "I studied computer science at MIT"
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddMemory; 