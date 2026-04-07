import { useState } from 'react'
import DashboardPage from './pages/DashboardPage'
import BrowsePage    from './pages/BrowsePage'
import JobsPage      from './pages/JobsPage'
import SearchPage    from './pages/SearchPage'

const NAV = [
  { key: 'dashboard', label: 'Dashboard',     icon: 'fa-chart-bar' },
  { key: 'search',    label: 'Search',        icon: 'fa-search' },
  { key: 'browse',    label: 'Browse Papers', icon: 'fa-book-open' },
  { key: 'jobs',      label: 'Jobs',          icon: 'fa-cogs' },
]

export default function App() {
  const [page, setPage] = useState('dashboard')

  return (
    <div id="wrapper">

      {/* Main Content */}
      <div id="main">
        <div className="inner">

          {/* Header */}
          <header id="header">
            <a href="#" className="logo">
              <strong>LitScope</strong> — IS Literature Explorer
            </a>
          </header>

          {/* Page Content */}
          {page === 'dashboard' && <DashboardPage />}
          {page === 'search'    && <SearchPage />}
          {page === 'browse'    && <BrowsePage />}
          {page === 'jobs'      && <JobsPage />}

        </div>
      </div>

      {/* Sidebar */}
      <div id="sidebar">
        <div className="inner">

          {/* Search */}
          <section id="search" className="alt">
            <form onSubmit={e => e.preventDefault()}>
              <input type="text" placeholder="Search" />
            </form>
          </section>

          {/* Navigation */}
          <nav id="menu">
            <header className="major">
              <h2>Menu</h2>
            </header>
            <ul>
              {NAV.map(n => (
                <li key={n.key}>
                  <a
                    href="#"
                    onClick={e => { e.preventDefault(); setPage(n.key) }}
                    style={{ fontWeight: page === n.key ? 700 : 'normal' }}
                  >
                    <span className={`icon solid ${n.icon}`} style={{ marginRight: 8 }} />
                    {n.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          {/* Footer */}
          <footer id="footer">
            <p className="copyright">
              &copy; LitScope. Built with <a href="https://html5up.net">HTML5 UP</a>.
            </p>
          </footer>

        </div>
      </div>

    </div>
  )
}
