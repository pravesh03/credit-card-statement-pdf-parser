import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { Upload, FileText, BarChart3, Settings } from 'lucide-react'
import UploadPage from './components/UploadPage'
import StatementsPage from './components/StatementsPage'
import StatementDetail from './components/StatementDetail'
import StatsPage from './components/StatsPage'
import { apiService } from './services/api'

function App() {
  const [statements, setStatements] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStatements()
  }, [])

  const loadStatements = async () => {
    try {
      const data = await apiService.getStatements()
      setStatements(data)
    } catch (error) {
      console.error('Failed to load statements:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStatementUploaded = (newStatement) => {
    setStatements(prev => [newStatement, ...prev])
  }

  return (
    <Router>
      <div className="min-h-screen">
        {/* Header */}
        <header className="bg-gradient-to-r from-slate-800 to-slate-700 backdrop-blur-md shadow-lg border-b border-gray-600/50 sticky top-0 z-50">
          <div className="container mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl shadow-lg">
                  <FileText className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Credit Card Statement Parser
                  </h1>
                  <p className="text-sm text-gray-300 font-medium">AI-Powered Document Processing</p>
                </div>
              </div>
              <nav className="flex items-center gap-2">
                <Link 
                  to="/" 
                  className="flex items-center gap-2 px-4 py-2 text-white hover:text-blue-200 hover:bg-blue-600/20 rounded-lg transition-all duration-200 font-medium"
                >
                  <Upload className="h-5 w-5" />
                  Upload
                </Link>
                <Link 
                  to="/statements" 
                  className="flex items-center gap-2 px-4 py-2 text-white hover:text-blue-200 hover:bg-blue-600/20 rounded-lg transition-all duration-200 font-medium"
                >
                  <FileText className="h-5 w-5" />
                  Statements
                </Link>
                <Link 
                  to="/stats" 
                  className="flex items-center gap-2 px-4 py-2 text-white hover:text-blue-200 hover:bg-blue-600/20 rounded-lg transition-all duration-200 font-medium"
                >
                  <BarChart3 className="h-5 w-5" />
                  Statistics
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-6 py-12">
          <div className="animate-fadeIn">
            <Routes>
              <Route 
                path="/" 
                element={
                  <UploadPage 
                    onStatementUploaded={handleStatementUploaded}
                  />
                } 
              />
              <Route 
                path="/statements" 
                element={
                  <StatementsPage 
                    statements={statements}
                    loading={loading}
                    onStatementsChange={loadStatements}
                  />
                } 
              />
              <Route 
                path="/statements/:id" 
                element={
                  <StatementDetail 
                    onStatementUpdate={loadStatements}
                  />
                } 
              />
              <Route 
                path="/stats" 
                element={<StatsPage />} 
              />
            </Routes>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-gradient-to-r from-slate-800 to-slate-700 backdrop-blur-md border-t border-gray-600/50 mt-20">
          <div className="container mx-auto px-6 py-8">
            <div className="text-center">
              <div className="flex items-center justify-center gap-3 mb-4">
                <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                  <FileText className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Credit Card Statement Parser
                </h3>
              </div>
            <p className="text-gray-300 font-medium mb-2">AI-Powered PDF Processing & Document Analysis</p>
            <p className="text-sm text-gray-400">
                Built with FastAPI, React, and OpenAI • 
                <span className="text-blue-600 font-semibold"> Production Ready</span>
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
