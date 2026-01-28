import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

// ═══════════════════════════════════════════════════════════════════════
// MEDIGUARD LANDING PAGE - Clinical Noir Theme
// Design: Dark, elegant, protective - "Bloomberg Terminal meets Medical"
// ═══════════════════════════════════════════════════════════════════════

// Particle Background Component
const ParticleBackground = () => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationId;
    let particles = [];
    
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    const createParticle = () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.5 + 0.1,
      pulse: Math.random() * Math.PI * 2
    });
    
    const init = () => {
      resize();
      particles = Array.from({ length: 80 }, createParticle);
    };
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach((p, i) => {
        p.x += p.vx;
        p.y += p.vy;
        p.pulse += 0.02;
        
        // Wrap around edges
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
        
        const pulseOpacity = p.opacity * (0.5 + Math.sin(p.pulse) * 0.5);
        
        // Draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 245, 212, ${pulseOpacity})`;
        ctx.fill();
        
        // Draw connections
        particles.slice(i + 1).forEach(p2 => {
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(0, 245, 212, ${0.1 * (1 - dist / 120)})`;
            ctx.stroke();
          }
        });
      });
      
      animationId = requestAnimationFrame(animate);
    };
    
    init();
    animate();
    window.addEventListener('resize', resize);
    
    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, []);
  
  return <canvas ref={canvasRef} className="particle-canvas" />;
};

// Guardian Icon Components
const GuardianIcon = ({ type }) => {
  const icons = {
    factkeeper: (
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M24 4L6 12v12c0 11 8 17 18 20 10-3 18-9 18-20V12L24 4z" />
        <path d="M16 24l6 6 10-12" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    sentinel: (
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="24" cy="24" r="18" />
        <path d="M24 14v10l6 6" strokeLinecap="round" />
        <circle cx="24" cy="24" r="4" fill="currentColor" />
      </svg>
    ),
    context: (
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="8" y="8" width="14" height="14" rx="2" />
        <rect x="26" y="8" width="14" height="14" rx="2" />
        <rect x="8" y="26" width="14" height="14" rx="2" />
        <rect x="26" y="26" width="14" height="14" rx="2" />
        <path d="M22 15h4M22 33h4M15 22v4M33 22v4" strokeLinecap="round" />
      </svg>
    ),
    quality: (
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M12 38V10h24v28" strokeLinecap="round" />
        <path d="M18 18h12M18 26h12M18 34h8" strokeLinecap="round" />
        <circle cx="36" cy="36" r="8" fill="none" />
        <path d="M33 36l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    calibrator: (
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="24" cy="24" r="18" />
        <path d="M24 14v10" strokeLinecap="round" />
        <path d="M16 32h16" strokeLinecap="round" />
        <circle cx="24" cy="24" r="3" />
        <path d="M24 6v4M24 38v4M6 24h4M38 24h4" strokeLinecap="round" />
      </svg>
    )
  };
  
  return <div className="guardian-icon">{icons[type]}</div>;
};

// Main Landing Page Component
export const LandingPage = () => {
  const [visibleSections, setVisibleSections] = useState(new Set());
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const sectionRefs = useRef({});
  const dashboardRef = useRef(null);
  
  // Intersection Observer for scroll animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setVisibleSections(prev => new Set([...prev, entry.target.id]));
          }
        });
      },
      { threshold: 0.1, rootMargin: '-50px' }
    );
    
    Object.values(sectionRefs.current).forEach(ref => {
      if (ref) observer.observe(ref);
    });
    
    return () => observer.disconnect();
  }, []);
  
  const isVisible = (id) => visibleSections.has(id);
  
  // 3D Tilt effect for dashboard preview
  const handleMouseMove = (e) => {
    if (!dashboardRef.current) return;
    const rect = dashboardRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const mouseX = e.clientX - centerX;
    const mouseY = e.clientY - centerY;
    
    // Calculate rotation (max 15 degrees)
    const rotateY = (mouseX / (rect.width / 2)) * 15;
    const rotateX = -(mouseY / (rect.height / 2)) * 10;
    
    setTilt({ x: rotateX, y: rotateY });
  };
  
  const handleMouseLeave = () => {
    setTilt({ x: 0, y: 0 });
  };

  // Problem Stories Data
  const problemStories = [
    {
      id: 'drug',
      title: 'The Midnight Drug Interaction',
      scenario: 'A patient asks your chatbot about taking St. John\'s Wort with their heart medication at 2am.',
      problem: 'Your AI says it\'s "probably fine."',
      reality: 'It\'s not. That combination could cause a stroke.',
      solution: 'MediGuard catches this in 340 milliseconds.',
      result: 'The patient gets a safe response instead.'
    },
    {
      id: 'emergency',
      title: 'The Missed Emergency',
      scenario: 'Someone describes chest pain and shortness of breath to your symptom checker.',
      problem: 'Your AI starts listing possible causes.',
      reality: 'None of them are "call 911 immediately."',
      solution: 'MediGuard flags the response.',
      result: 'A potentially life-saving escalation happens.'
    },
    {
      id: 'hallucination',
      title: 'The Confident Hallucination',
      scenario: 'Your AI confidently recommends a treatment protocol.',
      problem: 'It sounds authoritative. Specific. Professional.',
      reality: 'It\'s also completely fabricated.',
      solution: 'MediGuard verifies every claim against medical literature.',
      result: 'The hallucination never leaves the system.'
    }
  ];
  
  // Guardians Data
  const guardians = [
    {
      id: 'factkeeper',
      name: 'The Factkeeper',
      watches: 'Hallucinations & Fabrications',
      description: 'Every claim your AI makes gets verified against medical literature. Made-up facts don\'t get through.',
      color: '#3B82F6'
    },
    {
      id: 'sentinel',
      name: 'The Safety Sentinel',
      watches: 'Dangerous Advice',
      description: 'Medication errors, missed emergencies, harmful recommendations. We catch what could hurt someone.',
      color: '#FF6B6B'
    },
    {
      id: 'context',
      name: 'The Context Reader',
      watches: 'Misunderstandings',
      description: 'When someone asks about headaches and your AI talks about foot pain — we notice. Relevance matters.',
      color: '#F59E0B'
    },
    {
      id: 'quality',
      name: 'The Quality Auditor',
      watches: 'Incomplete Answers',
      description: 'Vague responses, missing information, half-answers. Your patients deserve complete guidance.',
      color: '#00F5D4'
    },
    {
      id: 'calibrator',
      name: 'The Confidence Calibrator',
      watches: 'False Certainty',
      description: 'AI that sounds sure when it shouldn\'t be. We flag overconfidence before it misleads.',
      color: '#A855F7'
    }
  ];
  
  // Process Steps Data
  const processSteps = [
    {
      step: 1,
      title: 'Capture',
      description: 'Patient asks, AI responds. We see everything — instantly.',
      detail: 'Millisecond-level latency. Shadow mode or intercept mode.'
    },
    {
      step: 2,
      title: 'Analyze',
      description: 'Five Guardians examine the response. Each one looking for different dangers.',
      detail: 'Parallel processing across all five dimensions simultaneously.'
    },
    {
      step: 3,
      title: 'Score',
      description: 'Risk calculated across all dimensions. Weighted for what matters most in healthcare.',
      detail: 'Weighted algorithm prioritizing safety (30%) and accuracy (25%).'
    },
    {
      step: 4,
      title: 'Decide',
      description: 'Safe? It goes through. Risky? It\'s flagged for review.',
      detail: 'Configurable thresholds. Your risk tolerance, your rules.'
    },
    {
      step: 5,
      title: 'Explain',
      description: 'Every flag comes with reasoning. Grounded in WHO, FDA, and peer-reviewed research.',
      detail: 'RAG-powered explanations with citations from 50+ medical guidelines.'
    }
  ];
  
  // Trust Stats Data
  const trustStats = [
    { value: '340', unit: 'ms', label: 'Average detection time' },
    { value: '18', unit: '', label: 'Unique safety flags monitored' },
    { value: '50', unit: '+', label: 'Medical guidelines in knowledge base' },
    { value: '99.2', unit: '%', label: 'Uptime across deployments' }
  ];

  // Smooth scroll handler
  const scrollToSection = (e, sectionId) => {
    e.preventDefault();
    const element = document.getElementById(sectionId);
    if (element) {
      const navbarHeight = 72;
      const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
      window.scrollTo({
        top: elementPosition - navbarHeight,
        behavior: 'smooth'
      });
    }
  };

  return (
    <div className="landing-page">
      {/* ═══════════════════════════════════════════════════════════════════
          NAVBAR
          ═══════════════════════════════════════════════════════════════════ */}
      <nav className="landing-navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-logo">
            <svg width="32" height="32" viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M24 4L6 12v12c0 11 8 17 18 20 10-3 18-9 18-20V12L24 4z" stroke="#00F5D4" />
              <path d="M16 24l6 6 10-12" stroke="#00F5D4" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span>MediGuard</span>
          </Link>
          
          <div className="navbar-links">
            <a href="#problems" onClick={(e) => scrollToSection(e, 'problems')} className="navbar-link">Why MediGuard</a>
            <a href="#guardians" onClick={(e) => scrollToSection(e, 'guardians')} className="navbar-link">How It Works</a>
            <a href="#dashboard" onClick={(e) => scrollToSection(e, 'dashboard')} className="navbar-link">Platform</a>
            <a href="#trust" onClick={(e) => scrollToSection(e, 'trust')} className="navbar-link">Trust</a>
          </div>
          
          <div className="navbar-actions">
            <Link to="/login" className="navbar-login">Log In</Link>
            <Link to="/signup" className="navbar-cta">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 1: HERO
          ═══════════════════════════════════════════════════════════════════ */}
      <section className="hero-section" id="hero" ref={el => sectionRefs.current.hero = el}>
        <ParticleBackground />
        <div className="hero-scanline" />
        
        <div className="hero-content">
          <div className="hero-badge">
            <span className="hero-badge-dot" />
            <span>AI Safety Platform</span>
          </div>
          
          <h1 className="hero-headline">
            <span className="hero-line hero-line-1">Your AI gives medical advice.</span>
            <span className="hero-line hero-line-2">Who's watching what it says?</span>
          </h1>
          
          <p className="hero-subline">
            MediGuard monitors every response your medical AI generates.
            <br />
            We catch unsafe advice before it reaches patients.
          </p>
          
          <div className="hero-cta-group">
            <Link to="/signup" className="hero-cta-primary">
              <span>Start Protecting Patients</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </Link>
            <a href="#guardians" onClick={(e) => scrollToSection(e, 'guardians')} className="hero-cta-secondary">
              See How It Works
            </a>
          </div>
          
          <div className="hero-pulse" />
        </div>
        
        <div className="hero-scroll-indicator" onClick={(e) => scrollToSection(e, 'problems')} style={{ cursor: 'pointer' }}>
          <span>Scroll to explore</span>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 5v14M5 12l7 7 7-7" />
          </svg>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 2: PROBLEM STORIES
          ═══════════════════════════════════════════════════════════════════ */}
      <section 
        className={`problems-section ${isVisible('problems') ? 'visible' : ''}`}
        id="problems"
        ref={el => sectionRefs.current.problems = el}
      >
        <div className="section-container">
          <div className="section-header">
            <span className="section-label">The Stakes</span>
            <h2 className="section-title">These aren't hypotheticals.</h2>
            <p className="section-subtitle">
              Real scenarios. Real risks. Every day, medical AI makes mistakes that could harm patients.
            </p>
          </div>
          
          <div className="problems-grid">
            {problemStories.map((story, index) => (
              <div 
                key={story.id} 
                className="problem-card"
                style={{ animationDelay: `${index * 0.15}s` }}
              >
                <div className="problem-card-content">
                  <h3 className="problem-title">{story.title}</h3>
                  
                  <div className="problem-scenario">
                    <p className="problem-text">{story.scenario}</p>
                  </div>
                  
                  <div className="problem-exchange">
                    <div className="exchange-problem">
                      <span className="exchange-label">The AI says:</span>
                      <p className="exchange-text danger">{story.problem}</p>
                    </div>
                    <div className="exchange-reality">
                      <span className="exchange-label">The reality:</span>
                      <p className="exchange-text">{story.reality}</p>
                    </div>
                  </div>
                  
                  <div className="problem-solution">
                    <div className="solution-shield">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" />
                        <path d="M9 12l2 2 4-4" />
                      </svg>
                    </div>
                    <div className="solution-text">
                      <p className="solution-action">{story.solution}</p>
                      <p className="solution-result">{story.result}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 3: FIVE GUARDIANS
          ═══════════════════════════════════════════════════════════════════ */}
      <section 
        className={`guardians-section ${isVisible('guardians') ? 'visible' : ''}`}
        id="guardians"
        ref={el => sectionRefs.current.guardians = el}
      >
        <div className="section-container">
          <div className="section-header">
            <span className="section-label">The Protection</span>
            <h2 className="section-title">Five Guardians. Five dimensions of safety.</h2>
            <p className="section-subtitle">
              Each one watching for different dangers. Together, they catch what humans miss.
            </p>
          </div>
          
          <div className="guardians-scroll">
            <div className="guardians-track">
              {guardians.map((guardian, index) => (
                <div 
                  key={guardian.id}
                  className="guardian-card"
                  style={{ 
                    '--guardian-color': guardian.color,
                    animationDelay: `${index * 0.1}s`
                  }}
                >
                  <div className="guardian-icon-wrapper" style={{ color: guardian.color }}>
                    <GuardianIcon type={guardian.id} />
                  </div>
                  <h3 className="guardian-name">{guardian.name}</h3>
                  <div className="guardian-watches">
                    <span className="watches-label">Watches for:</span>
                    <span className="watches-value">{guardian.watches}</span>
                  </div>
                  <p className="guardian-description">{guardian.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 4: SEVERITY SPECTRUM
          ═══════════════════════════════════════════════════════════════════ */}
      <section 
        className={`severity-section ${isVisible('severity') ? 'visible' : ''}`}
        id="severity"
        ref={el => sectionRefs.current.severity = el}
      >
        <div className="section-container">
          <div className="section-header">
            <span className="section-label">The Prioritization</span>
            <h2 className="section-title">Not every issue is an emergency.</h2>
            <p className="section-subtitle">
              We help you know the difference. Focus on what matters most.
            </p>
          </div>
          
          <div className="severity-content">
            <div className="severity-spectrum">
              <div className="severity-level severity-critical">
                <div className="severity-bar" />
                <div className="severity-info">
                  <div className="severity-header">
                    <span className="severity-badge critical">Critical</span>
                    <span className="severity-score">90-100%</span>
                  </div>
                  <p className="severity-action">"Stop everything. Review now."</p>
                  <p className="severity-description">Potential for immediate patient harm.</p>
                </div>
              </div>
              
              <div className="severity-level severity-high">
                <div className="severity-bar" />
                <div className="severity-info">
                  <div className="severity-header">
                    <span className="severity-badge high">High</span>
                    <span className="severity-score">75-89%</span>
                  </div>
                  <p className="severity-action">"Review within the hour."</p>
                  <p className="severity-description">Serious safety concerns requiring expert eyes.</p>
                </div>
              </div>
              
              <div className="severity-level severity-medium">
                <div className="severity-bar" />
                <div className="severity-info">
                  <div className="severity-header">
                    <span className="severity-badge medium">Medium</span>
                    <span className="severity-score">65-74%</span>
                  </div>
                  <p className="severity-action">"Review today."</p>
                  <p className="severity-description">Quality issues that need attention.</p>
                </div>
              </div>
              
              <div className="severity-level severity-low">
                <div className="severity-bar" />
                <div className="severity-info">
                  <div className="severity-header">
                    <span className="severity-badge low">Low</span>
                    <span className="severity-score">&lt; 65%</span>
                  </div>
                  <p className="severity-action">"Monitor and improve."</p>
                  <p className="severity-description">Minor concerns for continuous improvement.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 5: PROCESS FLOW
          ═══════════════════════════════════════════════════════════════════ */}
      <section 
        className={`process-section ${isVisible('process') ? 'visible' : ''}`}
        id="how-it-works"
        ref={el => sectionRefs.current.process = el}
      >
        <div className="section-container">
          <div className="section-header">
            <span className="section-label">The Process</span>
            <h2 className="section-title">From question to verified answer.</h2>
            <p className="section-subtitle">
              Every response analyzed in milliseconds. Here's what happens behind the scenes.
            </p>
          </div>
          
          <div className="process-timeline">
            {processSteps.map((step, index) => (
              <div 
                key={step.step}
                className="process-step"
                style={{ animationDelay: `${index * 0.12}s` }}
              >
                <div className="step-number">
                  <span>{step.step}</span>
                </div>
                <div className="step-content">
                  <h3 className="step-title">{step.title}</h3>
                  <p className="step-description">{step.description}</p>
                  <p className="step-detail">{step.detail}</p>
                </div>
                {index < processSteps.length - 1 && (
                  <div className="step-connector" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 6: DASHBOARD PREVIEW
          ═══════════════════════════════════════════════════════════════════ */}
      <section 
        className={`dashboard-section ${isVisible('dashboard') ? 'visible' : ''}`}
        id="dashboard"
        ref={el => sectionRefs.current.dashboard = el}
      >
        <div className="section-container">
          <div className="section-header">
            <span className="section-label">The Interface</span>
            <h2 className="section-title">See everything. Miss nothing.</h2>
            <p className="section-subtitle">
              Real-time monitoring. Clear prioritization. Complete audit trails for compliance.
            </p>
          </div>
          
          <div 
            className="dashboard-preview"
            ref={dashboardRef}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
          >
            <div 
              className="dashboard-frame"
              style={{
                transform: `perspective(1500px) rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
                transition: tilt.x === 0 && tilt.y === 0 ? 'transform 0.5s ease-out' : 'transform 0.1s ease-out'
              }}
            >
              <div className="dashboard-header-bar">
                <div className="dashboard-dots">
                  <span /><span /><span />
                </div>
                <span className="dashboard-url">mediguard.app/dashboard</span>
              </div>
              
              <div className="dashboard-content">
                <div className="dashboard-sidebar">
                  <div className="dash-nav-item active">
                    <span className="dash-icon">📊</span>
                    <span>Dashboard</span>
                  </div>
                  <div className="dash-nav-item">
                    <span className="dash-icon">🚨</span>
                    <span>Flagged</span>
                    <span className="dash-badge">12</span>
                  </div>
                  <div className="dash-nav-item">
                    <span className="dash-icon">💬</span>
                    <span>Interactions</span>
                  </div>
                  <div className="dash-nav-item">
                    <span className="dash-icon">📈</span>
                    <span>Analytics</span>
                  </div>
                </div>
                
                <div className="dashboard-main">
                  <div className="dash-stats-row">
                    <div className="dash-stat-card">
                      <span className="dash-stat-label">Total Today</span>
                      <span className="dash-stat-value">1,247</span>
                    </div>
                    <div className="dash-stat-card flagged">
                      <span className="dash-stat-label">Flagged</span>
                      <span className="dash-stat-value">23</span>
                    </div>
                    <div className="dash-stat-card">
                      <span className="dash-stat-label">Safe Rate</span>
                      <span className="dash-stat-value">98.2%</span>
                    </div>
                  </div>
                  
                  <div className="dash-activity">
                    <div className="dash-activity-header">
                      <span>Recent Flags</span>
                      <span className="dash-live-dot" />
                    </div>
                    <div className="dash-activity-list">
                      <div className="dash-activity-item critical">
                        <span className="activity-severity">Critical</span>
                        <span className="activity-text">Drug interaction warning missed</span>
                        <span className="activity-time">2m ago</span>
                      </div>
                      <div className="dash-activity-item high">
                        <span className="activity-severity">High</span>
                        <span className="activity-text">Emergency escalation needed</span>
                        <span className="activity-time">8m ago</span>
                      </div>
                      <div className="dash-activity-item medium">
                        <span className="activity-severity">Medium</span>
                        <span className="activity-text">Incomplete response detected</span>
                        <span className="activity-time">15m ago</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Callout annotations */}
            <div className="dashboard-callouts">
              <div className="callout callout-1">
                <span className="callout-line" />
                <span className="callout-text">Risk at a Glance</span>
              </div>
              <div className="callout callout-2">
                <span className="callout-line" />
                <span className="callout-text">Prioritized Queue</span>
              </div>
              <div className="callout callout-3">
                <span className="callout-line" />
                <span className="callout-text">Real-time Updates</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 7: TRUST SECTION
          ═══════════════════════════════════════════════════════════════════ */}
      <section 
        className={`trust-section ${isVisible('trust') ? 'visible' : ''}`}
        id="trust"
        ref={el => sectionRefs.current.trust = el}
      >
        <div className="section-container">
          <div className="trust-grid">
            <div className="trust-stats">
              {trustStats.map((stat, index) => (
                <div 
                  key={stat.label}
                  className="trust-stat"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="stat-value">
                    <span className="stat-number">{stat.value}</span>
                    <span className="stat-unit">{stat.unit}</span>
                  </div>
                  <span className="stat-label">{stat.label}</span>
                </div>
              ))}
            </div>
            
            <div className="trust-sources">
              <h3 className="trust-sources-title">Detection grounded in:</h3>
              <ul className="trust-sources-list">
                <li>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14" />
                    <path d="M12 5l7 7-7 7" />
                  </svg>
                  <span>WHO Clinical Guidelines</span>
                </li>
                <li>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14" />
                    <path d="M12 5l7 7-7 7" />
                  </svg>
                  <span>FDA Drug Safety Communications</span>
                </li>
                <li>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14" />
                    <path d="M12 5l7 7-7 7" />
                  </svg>
                  <span>Peer-reviewed medical literature</span>
                </li>
                <li>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14" />
                    <path d="M12 5l7 7-7 7" />
                  </svg>
                  <span>Healthcare compliance frameworks (HIPAA/GDPR)</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 8: CTA
          ═══════════════════════════════════════════════════════════════════ */}
      <section className="cta-section" id="cta">
        <div className="cta-glow" />
        <div className="section-container">
          <div className="cta-content">
            <h2 className="cta-headline">
              See MediGuard Protect Your AI
            </h2>
            <p className="cta-subtext">
              Your AI is one conversation away from being safer.
            </p>
            
            <div className="cta-buttons">
              <Link to="/signup" className="cta-primary">
                Schedule a Demo
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </Link>
              <Link to="/docs" className="cta-secondary">
                Explore Documentation
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                  <polyline points="15 3 21 3 21 9" />
                  <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════════
          SECTION 9: FOOTER
          ═══════════════════════════════════════════════════════════════════ */}
      <footer className="landing-footer">
        <div className="footer-container">
          <div className="footer-brand">
            <div className="footer-logo">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" />
              </svg>
              <span>MediGuard</span>
            </div>
            <p className="footer-tagline">Protecting medical AI, one response at a time.</p>
          </div>
          
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <a href="#guardians">How it Works</a>
              <a href="#severity">Risk Levels</a>
              <a href="#dashboard">Dashboard</a>
              <a href="/pricing">Pricing</a>
            </div>
            
            <div className="footer-column">
              <h4>Company</h4>
              <a href="/about">About</a>
              <a href="/contact">Contact</a>
              <a href="/careers">Careers</a>
              <a href="/press">Press</a>
            </div>
            
            <div className="footer-column">
              <h4>Resources</h4>
              <a href="/docs">Documentation</a>
              <a href="/api">API Reference</a>
              <a href="/security">Security</a>
              <a href="/compliance">Compliance</a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>© 2026 MediGuard. All rights reserved.</p>
          <div className="footer-legal">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
