import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Edit, Save, X, RefreshCw, FileText, AlertCircle } from 'lucide-react'
import { apiService } from '../services/api'
import { format } from 'date-fns'

const StatementDetail = ({ onStatementUpdate }) => {
  const { id } = useParams()
  const [statement, setStatement] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [editData, setEditData] = useState({})
  const [saving, setSaving] = useState(false)
  const [reprocessing, setReprocessing] = useState(false)

  useEffect(() => {
    loadStatement()
  }, [id])

  const loadStatement = async () => {
    try {
      const data = await apiService.getStatement(id)
      setStatement(data)
      setEditData({
        cardholder_name: data.cardholder_name || '',
        card_last_four: data.card_last_four || '',
        total_amount_due: data.total_amount_due || '',
        payment_due_date: data.payment_due_date ? format(new Date(data.payment_due_date), 'yyyy-MM-dd') : '',
        billing_period_start: data.billing_period_start ? format(new Date(data.billing_period_start), 'yyyy-MM-dd') : '',
        billing_period_end: data.billing_period_end ? format(new Date(data.billing_period_end), 'yyyy-MM-dd') : ''
      })
    } catch (error) {
      console.error('Failed to load statement:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = () => {
    setEditing(true)
  }

  const handleCancel = () => {
    setEditing(false)
    setEditData({
      cardholder_name: statement.cardholder_name || '',
      card_last_four: statement.card_last_four || '',
      total_amount_due: statement.total_amount_due || '',
      payment_due_date: statement.payment_due_date ? format(new Date(statement.payment_due_date), 'yyyy-MM-dd') : '',
      billing_period_start: statement.billing_period_start ? format(new Date(statement.billing_period_start), 'yyyy-MM-dd') : '',
      billing_period_end: statement.billing_period_end ? format(new Date(statement.billing_period_end), 'yyyy-MM-dd') : ''
    })
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const updateData = {
        cardholder_name: editData.cardholder_name || null,
        card_last_four: editData.card_last_four || null,
        total_amount_due: editData.total_amount_due ? parseFloat(editData.total_amount_due) : null,
        payment_due_date: editData.payment_due_date ? new Date(editData.payment_due_date).toISOString() : null,
        billing_period_start: editData.billing_period_start ? new Date(editData.billing_period_start).toISOString() : null,
        billing_period_end: editData.billing_period_end ? new Date(editData.billing_period_end).toISOString() : null
      }

      await apiService.updateStatement(id, updateData)
      await loadStatement()
      onStatementUpdate()
      setEditing(false)
    } catch (error) {
      console.error('Failed to update statement:', error)
      alert('Failed to update statement')
    } finally {
      setSaving(false)
    }
  }

  const handleReprocess = async () => {
    setReprocessing(true)
    try {
      await apiService.reprocessStatement(id)
      await loadStatement()
      onStatementUpdate()
    } catch (error) {
      console.error('Failed to reprocess statement:', error)
      alert('Failed to reprocess statement')
    } finally {
      setReprocessing(false)
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

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="loading h-8 w-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading statement details...</p>
        </div>
      </div>
    )
  }

  if (!statement) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Statement not found
        </h3>
        <p className="text-gray-600 mb-4">
          The statement you're looking for doesn't exist or has been deleted.
        </p>
        <Link to="/statements" className="btn btn-primary">
          Back to Statements
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <Link to="/statements" className="btn btn-secondary">
          <ArrowLeft className="h-4 w-4" />
          Back
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gray-900">
            {statement.filename}
          </h1>
          <p className="text-gray-600">
            {statement.issuer?.toUpperCase() || 'Unknown Issuer'} • 
            Uploaded {formatDate(statement.created_at)}
          </p>
        </div>
        <div className="flex gap-2">
          {!editing ? (
            <>
              <button
                onClick={handleEdit}
                className="btn btn-secondary"
              >
                <Edit className="h-4 w-4" />
                Edit
              </button>
              <button
                onClick={handleReprocess}
                disabled={reprocessing}
                className="btn btn-primary"
              >
                {reprocessing ? (
                  <div className="loading h-4 w-4"></div>
                ) : (
                  <RefreshCw className="h-4 w-4" />
                )}
                Reprocess
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleCancel}
                className="btn btn-secondary"
              >
                <X className="h-4 w-4" />
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="btn btn-success"
              >
                {saving ? (
                  <div className="loading h-4 w-4"></div>
                ) : (
                  <Save className="h-4 w-4" />
                )}
                Save
              </button>
            </>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Statement Information */}
        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold">Statement Information</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="form-label">Cardholder Name</label>
              {editing ? (
                <input
                  type="text"
                  value={editData.cardholder_name}
                  onChange={(e) => setEditData({...editData, cardholder_name: e.target.value})}
                  className="form-input"
                />
              ) : (
                <p className="text-lg font-medium">
                  {statement.cardholder_name || 'N/A'}
                </p>
              )}
            </div>

            <div>
              <label className="form-label">Card Last 4 Digits</label>
              {editing ? (
                <input
                  type="text"
                  value={editData.card_last_four}
                  onChange={(e) => setEditData({...editData, card_last_four: e.target.value})}
                  className="form-input"
                  maxLength="4"
                />
              ) : (
                <p className="text-lg font-medium">
                  {statement.card_last_four || 'N/A'}
                </p>
              )}
            </div>

            <div>
              <label className="form-label">Total Amount Due</label>
              {editing ? (
                <input
                  type="number"
                  step="0.01"
                  value={editData.total_amount_due}
                  onChange={(e) => setEditData({...editData, total_amount_due: e.target.value})}
                  className="form-input"
                />
              ) : (
                <p className="text-lg font-medium text-red-600">
                  {formatCurrency(statement.total_amount_due)}
                </p>
              )}
            </div>

            <div>
              <label className="form-label">Payment Due Date</label>
              {editing ? (
                <input
                  type="date"
                  value={editData.payment_due_date}
                  onChange={(e) => setEditData({...editData, payment_due_date: e.target.value})}
                  className="form-input"
                />
              ) : (
                <p className="text-lg font-medium">
                  {formatDate(statement.payment_due_date)}
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="form-label">Billing Period Start</label>
                {editing ? (
                  <input
                    type="date"
                    value={editData.billing_period_start}
                    onChange={(e) => setEditData({...editData, billing_period_start: e.target.value})}
                    className="form-input"
                  />
                ) : (
                  <p className="font-medium">
                    {formatDate(statement.billing_period_start)}
                  </p>
                )}
              </div>
              <div>
                <label className="form-label">Billing Period End</label>
                {editing ? (
                  <input
                    type="date"
                    value={editData.billing_period_end}
                    onChange={(e) => setEditData({...editData, billing_period_end: e.target.value})}
                    className="form-input"
                  />
                ) : (
                  <p className="font-medium">
                    {formatDate(statement.billing_period_end)}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Extraction Details */}
        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold">Extraction Details</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="form-label">Overall Confidence</label>
              <div className="flex items-center gap-2">
                <div className={`badge ${getConfidenceBadge(statement.overall_confidence)}`}>
                  {Math.round((statement.overall_confidence || 0) * 100)}%
                </div>
                <span className={getConfidenceColor(statement.overall_confidence)}>
                  {statement.overall_confidence >= 0.8 ? 'High' : 
                   statement.overall_confidence >= 0.6 ? 'Medium' : 'Low'}
                </span>
              </div>
            </div>

            <div>
              <label className="form-label">Extraction Method</label>
              <p className="font-medium">
                {statement.extraction_method || 'Unknown'}
              </p>
            </div>

            <div>
              <label className="form-label">Processing Status</label>
              <div className="flex gap-2">
                <div className={`badge ${statement.is_processed ? 'badge-success' : 'badge-warning'}`}>
                  {statement.is_processed ? 'Processed' : 'Pending'}
                </div>
                {statement.has_errors && (
                  <div className="badge badge-error">Has Errors</div>
                )}
              </div>
            </div>

            {statement.llm_rationale && (
              <div>
                <label className="form-label">AI Analysis</label>
                <div className="p-3 bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg border border-blue-500/20">
                  <p className="text-sm text-blue-100">
                    {statement.llm_rationale}
                  </p>
                </div>
              </div>
            )}

            {statement.error_message && (
              <div>
                <label className="form-label">Error Message</label>
                <div className="p-3 bg-red-50 rounded-lg">
                  <p className="text-sm text-red-800">
                    {statement.error_message}
                  </p>
                </div>
              </div>
            )}

            <div className="flex gap-2">
              <a
                href={`http://localhost:8000/${statement.file_path}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
              >
                <FileText className="h-4 w-4" />
                View PDF
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Field Confidence Scores */}
      {statement.extraction_steps && (
        <div className="card mt-6">
          <div className="card-header">
            <h2 className="text-xl font-semibold">Field Confidence Scores</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(statement.extraction_steps).map(([field, steps]) => (
              <div key={field} className="p-3 border rounded-lg">
                <h4 className="font-semibold text-sm mb-1 capitalize">
                  {field.replace(/_/g, ' ')}
                </h4>
                <p className="text-xs text-gray-600">
                  {typeof steps === 'string' ? steps : 'Extracted successfully'}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default StatementDetail
