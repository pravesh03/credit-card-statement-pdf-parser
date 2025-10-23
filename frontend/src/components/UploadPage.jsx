import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, AlertCircle, CheckCircle, Loader } from 'lucide-react'
import { apiService } from '../services/api'
import { format } from 'date-fns'

const UploadPage = ({ onStatementUploaded }) => {
  const [uploading, setUploading] = useState(false)
  const [uploadResults, setUploadResults] = useState([])
  const [selectedIssuer, setSelectedIssuer] = useState('')
  const [dragActive, setDragActive] = useState(false)

  const issuers = [
    { value: '', label: 'Auto-detect' },
    { value: 'hdfc', label: 'HDFC Bank' },
    { value: 'sbi', label: 'State Bank of India' },
    { value: 'icici', label: 'ICICI Bank' },
    { value: 'axis', label: 'Axis Bank' },
    { value: 'citibank', label: 'Citibank' }
  ]

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return

    setUploading(true)
    setUploadResults([])

    try {
      if (acceptedFiles.length === 1) {
        // Single file upload
        const result = await apiService.uploadStatement(acceptedFiles[0], selectedIssuer || null)
        setUploadResults([result])
        onStatementUploaded(result)
      } else {
        // Batch upload
        const result = await apiService.uploadBatch(acceptedFiles, selectedIssuer || null)
        setUploadResults(result.results || [])
        result.results?.forEach(stmt => onStatementUploaded(stmt))
      }
    } catch (error) {
      console.error('Upload failed:', error)
      setUploadResults([{
        error: error.response?.data?.detail || error.message || 'Upload failed'
      }])
    } finally {
      setUploading(false)
    }
  }, [selectedIssuer, onStatementUploaded])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true,
    onDragEnter: () => setDragActive(true),
    onDragLeave: () => setDragActive(false),
    onDropAccepted: () => setDragActive(false),
    onDropRejected: () => setDragActive(false)
  })

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

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">
          Upload Credit Card Statements
        </h1>
        <p className="text-xl mb-2">
          AI-Powered PDF Processing & Document Analysis
        </p>
        <p className="text-sm">
          Supports HDFC, SBI, ICICI, Axis, Citibank and more
        </p>
      </div>

      {/* Upload Form */}
      <div className="card mb-8">
        <div className="card-header">
          <h2 className="text-2xl font-bold flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Upload className="h-6 w-6 text-white" />
            </div>
            File Upload
          </h2>
        </div>
        
        <div className="mb-6">
          <label className="form-label">Bank/Issuer (Optional)</label>
          <select
            value={selectedIssuer}
            onChange={(e) => setSelectedIssuer(e.target.value)}
            className="form-select"
          >
            {issuers.map(issuer => (
              <option key={issuer.value} value={issuer.value}>
                {issuer.label}
              </option>
            ))}
          </select>
        </div>

        <div
          {...getRootProps()}
          className={`upload-area ${isDragActive || dragActive ? 'dragover' : ''} ${
            uploadResults.length > 0 ? 'has-files' : ''
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center gap-4">
            {uploading ? (
              <>
                <div className="p-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full">
                  <Loader className="h-12 w-12 text-blue-600 animate-spin" />
                </div>
                <div>
                  <p className="text-lg font-semibold">Processing...</p>
                  <p className="text-sm">Extracting information from your PDF</p>
                </div>
              </>
            ) : (
              <>
                <div className="p-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full">
                  <Upload className="h-12 w-12 text-blue-600" />
                </div>
                <div>
                  <p className="text-lg font-semibold">
                    {isDragActive ? 'Drop files here' : 'Drag & drop PDF files here'}
                  </p>
                  <p className="text-sm">
                    or click to select files (supports multiple files)
                  </p>
                </div>
                <button className="btn btn-primary">
                  <Upload className="h-5 w-5" />
                  Select Files
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Upload Results */}
      {uploadResults.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold">Extraction Results</h2>
          </div>
          
          <div className="space-y-4">
            {uploadResults.map((result, index) => (
              <div key={index} className="upload-result">
                {result.error ? (
                  <div className="alert alert-error">
                    <AlertCircle className="h-5 w-5" />
                    <div>
                      <p className="font-semibold">Upload Failed</p>
                      <p className="text-sm">{result.error}</p>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <FileText className="h-8 w-8 text-blue-600" />
                        <div>
                          <h3 className="font-semibold">{result.filename}</h3>
                          <p className="text-sm">
                            Statement ID: {result.statement_id}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`badge ${getConfidenceBadge(result.extraction_result.overall_confidence)}`}>
                          {Math.round(result.extraction_result.overall_confidence * 100)}% Confidence
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">Extracted Information</h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="font-medium">Cardholder Name:</span>
                            <span className="font-semibold">
                              {result.extraction_result.cardholder_name || 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="font-medium">Card Last 4:</span>
                            <span className="font-semibold">
                              {result.extraction_result.card_last_four || 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="font-medium">Billing Period:</span>
                            <span className="font-semibold">
                              {result.extraction_result.billing_period_start && result.extraction_result.billing_period_end
                                ? `${formatDate(result.extraction_result.billing_period_start)} - ${formatDate(result.extraction_result.billing_period_end)}`
                                : 'N/A'
                              }
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="font-medium">Payment Due Date:</span>
                            <span className="font-semibold">
                              {formatDate(result.extraction_result.payment_due_date)}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="font-medium">Total Amount Due:</span>
                            <span className="font-semibold text-red-600">
                              {formatCurrency(result.extraction_result.total_amount_due)}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div>
                        <h4 className="font-semibold mb-2">Field Confidence</h4>
                        <div className="space-y-2">
                          {Object.entries(result.extraction_result.confidence_scores).map(([field, confidence]) => (
                            <div key={field} className="flex justify-between items-center">
                              <span className="text-sm font-medium capitalize">
                                {field.replace(/_/g, ' ')}:
                              </span>
                              <span className={`text-sm font-semibold ${getConfidenceColor(confidence)}`}>
                                {Math.round(confidence * 100)}%
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    {result.extraction_result.llm_rationale && (
                      <div className="mt-4 p-3 bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg border border-blue-500/20">
                        <h5 className="font-semibold text-blue-200 mb-1">AI Analysis</h5>
                        <p className="text-sm text-blue-100">
                          {result.extraction_result.llm_rationale}
                        </p>
                      </div>
                    )}

                    <div className="mt-4 flex gap-2">
                      <a
                        href={result.file_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-secondary"
                      >
                        View PDF
                      </a>
                      <button
                        onClick={() => window.location.href = `/statements/${result.statement_id}`}
                        className="btn btn-primary"
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default UploadPage
