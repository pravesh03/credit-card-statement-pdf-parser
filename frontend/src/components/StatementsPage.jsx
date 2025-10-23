import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FileText, Eye, Trash2, RefreshCw, Filter, Search } from 'lucide-react'
import { apiService } from '../services/api'
import { format } from 'date-fns'

const StatementsPage = ({ statements, loading, onStatementsChange }) => {
  const [filteredStatements, setFilteredStatements] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [issuerFilter, setIssuerFilter] = useState('')
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState('desc')
  const [deleting, setDeleting] = useState(null)

  useEffect(() => {
    setFilteredStatements(statements)
  }, [statements])

  useEffect(() => {
    let filtered = [...statements]

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(stmt =>
        stmt.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
        stmt.cardholder_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        stmt.card_last_four?.includes(searchTerm)
      )
    }

    // Issuer filter
    if (issuerFilter) {
      filtered = filtered.filter(stmt => stmt.issuer === issuerFilter)
    }

    // Sort
    filtered.sort((a, b) => {
      let aVal = a[sortBy]
      let bVal = b[sortBy]

      if (sortBy === 'created_at' || sortBy === 'updated_at') {
        aVal = new Date(aVal)
        bVal = new Date(bVal)
      }

      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1
      } else {
        return aVal < bVal ? 1 : -1
      }
    })

    setFilteredStatements(filtered)
  }, [statements, searchTerm, issuerFilter, sortBy, sortOrder])

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this statement?')) return

    setDeleting(id)
    try {
      await apiService.deleteStatement(id)
      onStatementsChange()
    } catch (error) {
      console.error('Delete failed:', error)
      alert('Failed to delete statement')
    } finally {
      setDeleting(null)
    }
  }

  const handleReprocess = async (id) => {
    try {
      await apiService.reprocessStatement(id)
      onStatementsChange()
    } catch (error) {
      console.error('Reprocess failed:', error)
      alert('Failed to reprocess statement')
    }
  }

  const formatCurrency = (amount) => {
    if (amount === null || amount === undefined) return 'N/A'
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR'
    }).format(amount)
  }

  const formatDate = (date) => {
    if (!date) return 'N/A'
    return format(new Date(date), 'dd/MM/yyyy')
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600'
    if (confidence >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getConfidenceBadge = (confidence) => {
    if (confidence >= 0.8) return 'badge-success'
    if (confidence >= 0.6) return 'badge-warning'
    return 'badge-error'
  }

  const getStatusBadge = (stmt) => {
    if (stmt.has_errors) return 'badge-error'
    if (stmt.is_processed) return 'badge-success'
    return 'badge-warning'
  }

  const getStatusText = (stmt) => {
    if (stmt.has_errors) return 'Error'
    if (stmt.is_processed) return 'Processed'
    return 'Pending'
  }

  const issuers = [...new Set(statements.map(s => s.issuer).filter(Boolean))]

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="loading h-8 w-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading statements...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
          Credit Card Statements
        </h1>
        <p className="text-xl text-gray-600 font-medium">
          Manage and view your processed statements
        </p>
      </div>

      {/* Filters */}
      <div className="card mb-8">
        <div className="card-header">
          <h2 className="text-xl font-bold text-gray-800 flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Filter className="h-5 w-5 text-white" />
            </div>
            Filters & Search
          </h2>
        </div>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by filename, cardholder name, or last 4 digits..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="form-input pl-10"
              />
            </div>
          </div>
          <div className="md:w-48">
            <select
              value={issuerFilter}
              onChange={(e) => setIssuerFilter(e.target.value)}
              className="form-select"
            >
              <option value="">All Issuers</option>
              {issuers.map(issuer => (
                <option key={issuer} value={issuer}>
                  {issuer.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
          <div className="md:w-48">
            <select
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [field, order] = e.target.value.split('-')
                setSortBy(field)
                setSortOrder(order)
              }}
              className="form-select"
            >
              <option value="created_at-desc">Newest First</option>
              <option value="created_at-asc">Oldest First</option>
              <option value="filename-asc">Name A-Z</option>
              <option value="filename-desc">Name Z-A</option>
              <option value="overall_confidence-desc">High Confidence</option>
              <option value="overall_confidence-asc">Low Confidence</option>
            </select>
          </div>
        </div>
      </div>

      {/* Statements List */}
      {filteredStatements.length === 0 ? (
        <div className="card text-center py-12">
          <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No statements found
          </h3>
          <p className="text-gray-600 mb-4">
            {searchTerm || issuerFilter
              ? 'Try adjusting your search criteria'
              : 'Upload your first credit card statement to get started'
            }
          </p>
          <Link to="/" className="btn btn-primary">
            Upload Statement
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredStatements.map((statement) => (
            <div key={statement.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <FileText className="h-8 w-8 text-blue-600" />
                  <div>
                    <h3 className="font-semibold text-gray-900 truncate">
                      {statement.filename}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {statement.issuer?.toUpperCase() || 'Unknown Issuer'}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <div className={`badge ${getConfidenceBadge(statement.overall_confidence)}`}>
                    {Math.round((statement.overall_confidence || 0) * 100)}%
                  </div>
                  <div className={`badge ${getStatusBadge(statement)}`}>
                    {getStatusText(statement)}
                  </div>
                </div>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Cardholder:</span>
                  <span className="font-medium">
                    {statement.cardholder_name || 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Card Last 4:</span>
                  <span className="font-medium">
                    {statement.card_last_four || 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Amount Due:</span>
                  <span className="font-medium text-red-600">
                    {formatCurrency(statement.total_amount_due)}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Due Date:</span>
                  <span className="font-medium">
                    {formatDate(statement.payment_due_date)}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>Uploaded {formatDate(statement.created_at)}</span>
                <span className={getConfidenceColor(statement.overall_confidence)}>
                  {Math.round((statement.overall_confidence || 0) * 100)}% confidence
                </span>
              </div>

              <div className="flex gap-2">
                <Link
                  to={`/statements/${statement.id}`}
                  className="btn btn-primary flex-1"
                >
                  <Eye className="h-4 w-4" />
                  View Details
                </Link>
                <button
                  onClick={() => handleReprocess(statement.id)}
                  className="btn btn-secondary"
                  title="Reprocess"
                >
                  <RefreshCw className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleDelete(statement.id)}
                  disabled={deleting === statement.id}
                  className="btn btn-danger"
                  title="Delete"
                >
                  {deleting === statement.id ? (
                    <div className="loading h-4 w-4"></div>
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Summary */}
      {filteredStatements.length > 0 && (
        <div className="mt-8 text-center text-gray-600">
          Showing {filteredStatements.length} of {statements.length} statements
        </div>
      )}
    </div>
  )
}

export default StatementsPage
