# Admin Components Integration Guide

## Quick Start

### 1. Import Components
```jsx
import Dashboard from './pages/admin/Dashboard';
import InteractionDetail from './pages/admin/InteractionDetail';
```

### 2. Add Routes (Already Done in App.jsx)
```jsx
<Route 
  path="/admin/dashboard" 
  element={<AdminRoute><Dashboard /></AdminRoute>} 
/>
<Route 
  path="/admin/interactions/:id" 
  element={<AdminRoute><InteractionDetail /></AdminRoute>} 
/>
```

---

## Replace Mock Data with Real API

### Dashboard.jsx - Stats Data

**Current Mock:**
```javascript
const stats = [
  { label: 'Total Interactions', value: '12,847', change: '+12.5%', direction: 'up' },
  // ...
];
```

**Replace with API call:**
```javascript
import { useEffect, useState } from 'react';

const Dashboard = () => {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/admin/stats');
        const data = await response.json();
        setStats([
          {
            label: 'Total Interactions',
            value: data.total_interactions.toLocaleString(),
            change: `${data.total_interactions_change > 0 ? '+' : ''}${data.total_interactions_change}%`,
            direction: data.total_interactions_change > 0 ? 'up' : 'down'
          },
          // Map other stats...
        ]);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  // ... rest of component
};
```

---

### InteractionDetail.jsx - Interaction Data

**Current Mock:**
```javascript
const interaction = {
  id: id || 'INT-2026-001234',
  timestamp: '2026-01-27 14:32:15 UTC',
  // ...
};
```

**Replace with API call:**
```javascript
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const InteractionDetail = () => {
  const { id } = useParams();
  const [interaction, setInteraction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInteraction = async () => {
      try {
        const response = await fetch(`/api/admin/interactions/${id}`);
        if (!response.ok) throw new Error('Interaction not found');
        const data = await response.json();
        setInteraction(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInteraction();
  }, [id]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  // ... rest of component
};
```

---

## Expected API Response Formats

### GET `/api/admin/stats`
```json
{
  "total_interactions": 12847,
  "total_interactions_change": 12.5,
  "flagged_cases": 342,
  "flagged_cases_change": -5.2,
  "pending_reviews": 28,
  "pending_reviews_change": 8.1,
  "avg_response_time": "1.2s",
  "avg_response_time_change": -15.3
}
```

### GET `/api/admin/interactions/:id`
```json
{
  "id": "INT-2026-001234",
  "timestamp": "2026-01-27T14:32:15Z",
  "model": "gpt-4-medical-v2",
  "user_id": "user_7x9k2m",
  "user_input": "What are the potential side effects...",
  "ai_response": "While both aspirin and ibuprofen...",
  "topics": ["medication_interactions", "nsaids", "safety_concerns"],
  "flags": {
    "contains_medical_advice": true,
    "references_specific_medications": true,
    "suggests_doctor_consultation": true,
    "contains_disclaimers": false,
    "potential_harm": false,
    "off_topic": false
  },
  "scores": {
    "toxicity": 0.12,
    "medical_accuracy": 0.85,
    "safety_risk": 0.34
  },
  "overall_score": 0.34,
  "status": "flagged",
  "explanation": "The response provides generally accurate...",
  "citations": [
    {
      "title": "NSAID Drug Interactions - Clinical Guidelines",
      "source": "medical_guidelines/nsaid_interactions.pdf",
      "relevance": 0.94
    }
  ],
  "review": {
    "status": "safe",
    "reviewer": "Dr. Sarah Mitchell",
    "timestamp": "2026-01-27T15:45:00Z",
    "corrected_response": "While both aspirin and ibuprofen...",
    "comments": "Response is medically accurate..."
  }
}
```

---

## Adding Loading States

### Skeleton Cards for Stats
```jsx
import './components/common/LoadingSpinner.css'; // Assuming you have skeleton styles

const StatsGridSkeleton = () => (
  <div className="admin-stats-grid">
    {[1, 2, 3, 4].map(i => (
      <div key={i} className="admin-stat-card">
        <div className="skeleton skeleton-text" style={{ width: '60%', height: '14px' }} />
        <div className="skeleton skeleton-text" style={{ width: '80%', height: '30px', marginTop: '8px' }} />
        <div className="skeleton skeleton-text" style={{ width: '40%', height: '14px', marginTop: '8px' }} />
      </div>
    ))}
  </div>
);

// In Dashboard component:
{loading ? <StatsGridSkeleton /> : <div className="admin-stats-grid">...</div>}
```

### Skeleton for Interaction Detail
```jsx
const InteractionDetailSkeleton = () => (
  <div className="interaction-detail">
    <div className="interaction-detail-header">
      <div className="skeleton skeleton-text" style={{ width: '200px', height: '24px' }} />
      <div className="skeleton skeleton-text" style={{ width: '150px', height: '20px' }} />
    </div>
    {[1, 2, 3, 4, 5].map(level => (
      <div key={level} className="level-section">
        <div className="level-header">
          <div className="skeleton skeleton-avatar" style={{ width: '32px', height: '32px' }} />
          <div style={{ flex: 1 }}>
            <div className="skeleton skeleton-text" style={{ width: '40%', height: '18px' }} />
            <div className="skeleton skeleton-text" style={{ width: '60%', height: '14px', marginTop: '4px' }} />
          </div>
        </div>
        <div className="level-content">
          <div className="skeleton skeleton-text" style={{ width: '100%', height: '100px' }} />
        </div>
      </div>
    ))}
  </div>
);
```

---

## Error Handling

### Error State Component
```jsx
const ErrorState = ({ message, onRetry }) => (
  <div style={{ 
    textAlign: 'center', 
    padding: 'var(--space-10)',
    color: 'var(--color-danger-text)'
  }}>
    <div style={{ 
      fontSize: '48px', 
      marginBottom: 'var(--space-4)' 
    }}>⚠️</div>
    <h3 style={{ 
      fontFamily: 'var(--font-display)', 
      fontSize: 'var(--text-xl)',
      marginBottom: 'var(--space-2)' 
    }}>Error Loading Data</h3>
    <p style={{ 
      color: 'var(--color-slate-600)', 
      marginBottom: 'var(--space-4)' 
    }}>{message}</p>
    {onRetry && (
      <button className="btn btn-primary" onClick={onRetry}>
        Try Again
      </button>
    )}
  </div>
);

// Usage:
if (error) {
  return <ErrorState message={error} onRetry={() => window.location.reload()} />;
}
```

---

## Navigation Integration

### From Dashboard to Interaction Detail
```jsx
// In future components (e.g., AdminAllInteractions table)
import { Link } from 'react-router-dom';

const InteractionRow = ({ interaction }) => (
  <tr>
    <td>{interaction.id}</td>
    <td>{interaction.timestamp}</td>
    <td>
      <Link 
        to={`/admin/interactions/${interaction.id}`}
        className="btn btn-sm btn-outline"
      >
        View Details
      </Link>
    </td>
  </tr>
);
```

### Programmatic Navigation
```jsx
import { useNavigate } from 'react-router-dom';

const SomeComponent = () => {
  const navigate = useNavigate();

  const handleViewInteraction = (id) => {
    navigate(`/admin/interactions/${id}`);
  };

  return (
    <button onClick={() => handleViewInteraction('INT-123')}>
      View Interaction
    </button>
  );
};
```

---

## Customization

### Change Sidebar Items
Edit `navSections` array in `Dashboard.jsx`:

```javascript
const navSections = [
  {
    title: 'Your Section',
    items: [
      { 
        icon: '📊',          // Any emoji or icon
        label: 'Your Page', 
        path: '/admin/your-page', 
        active: true,        // Highlight this item
        badge: '5'           // Optional notification badge
      }
    ]
  }
];
```

### Adjust Colors
All colors use CSS variables from `variables.css`. To change theme:

```css
/* In variables.css or override in component CSS */
:root {
  --color-primary-500: #your-brand-color;
  --color-flagged-main: #your-alert-color;
}
```

### Add Custom Stats
```javascript
const stats = [
  ...existingStats,
  {
    label: 'Your Custom Metric',
    value: '99.9%',
    change: '+2.1%',
    direction: 'up'
  }
];
```

---

## Accessibility Improvements

### Add ARIA Labels
```jsx
<button 
  className="mobile-menu-btn"
  onClick={() => setSidebarOpen(!sidebarOpen)}
  aria-label={sidebarOpen ? 'Close menu' : 'Open menu'}
  aria-expanded={sidebarOpen}
>
  {sidebarOpen ? '✕' : '☰'}
</button>

<nav className="admin-sidebar-nav" aria-label="Main navigation">
  {/* Navigation items */}
</nav>
```

### Keyboard Navigation
```jsx
const handleKeyDown = (e, path) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    navigate(path);
  }
};

<div 
  className="admin-nav-item"
  onClick={() => navigate(path)}
  onKeyDown={(e) => handleKeyDown(e, path)}
  role="button"
  tabIndex={0}
>
  {/* Item content */}
</div>
```

---

## Performance Optimization

### Code Splitting
```jsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/admin/Dashboard'));
const InteractionDetail = lazy(() => import('./pages/admin/InteractionDetail'));

// In routes:
<Route 
  path="/admin/dashboard" 
  element={
    <Suspense fallback={<LoadingSpinner />}>
      <AdminRoute><Dashboard /></AdminRoute>
    </Suspense>
  } 
/>
```

### Memoize Expensive Calculations
```jsx
import { useMemo } from 'react';

const InteractionDetail = () => {
  const scoreLevel = useMemo(() => {
    return (score) => {
      if (score < 0.3) return 'low';
      if (score < 0.7) return 'medium';
      return 'high';
    };
  }, []);

  // Use scoreLevel function...
};
```

---

## Testing

### Component Tests (Jest + React Testing Library)
```jsx
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from './Dashboard';

test('renders dashboard with stats', () => {
  render(
    <BrowserRouter>
      <Dashboard />
    </BrowserRouter>
  );
  
  expect(screen.getByText('Dashboard Overview')).toBeInTheDocument();
  expect(screen.getByText('Total Interactions')).toBeInTheDocument();
});
```

### Responsive Testing
```jsx
import { render } from '@testing-library/react';

test('mobile menu button visible on small screens', () => {
  global.innerWidth = 500;
  global.dispatchEvent(new Event('resize'));
  
  const { container } = render(<Dashboard />);
  const menuBtn = container.querySelector('.mobile-menu-btn');
  
  expect(menuBtn).toBeVisible();
});
```

---

**Need Help?** Refer to:
- Design spec: `FRONTEND_DESIGN_DOCUMENT.md`
- Implementation summary: `PHASE_6_IMPLEMENTATION_SUMMARY.md`
- Component styles: `frontend/src/pages/admin/*.css`
