import React, { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, FileText, AlertCircle, CheckCircle, Clock } from 'lucide-react'
import { apiService } from '../services/api'

const StatsPage = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await apiService.getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-IN').format(num)
  }

  const formatPercentage = (num) => {
    return `${Math.round(num * 100)}%`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="loading h-8 w-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading statistics...</p>
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Failed to load statistics
        </h3>
        <p className="text-gray-600 mb-4">
          There was an error loading the statistics data.
        </p>
        <button onClick={loadStats} className="btn btn-primary">
          Try Again
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Processing Statistics
        </h1>
        <p className="text-gray-600">
          Overview of credit card statement processing performance
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="h-8 w-8 text-blue-600" />
            <h3 className="text-lg font-semibold">Total Statements</h3>
          </div>
          <p className="text-3xl font-bold text-blue-600">
            {formatNumber(stats.total_statements)}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            All uploaded statements
          </p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <h3 className="text-lg font-semibold">Processed</h3>
          </div>
          <p className="text-3xl font-bold text-green-600">
            {formatNumber(stats.processed_statements)}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            {formatPercentage(stats.processed_statements / Math.max(stats.total_statements, 1))} success rate
          </p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <AlertCircle className="h-8 w-8 text-red-600" />
            <h3 className="text-lg font-semibold">Errors</h3>
          </div>
          <p className="text-3xl font-bold text-red-600">
            {formatNumber(stats.error_statements)}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            {formatPercentage(stats.error_statements / Math.max(stats.total_statements, 1))} error rate
          </p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="h-8 w-8 text-purple-600" />
            <h3 className="text-lg font-semibold">Avg Confidence</h3>
          </div>
          <p className="text-3xl font-bold text-purple-600">
            {formatPercentage(stats.average_confidence)}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            Average extraction confidence
          </p>
        </div>
      </div>

      {/* Issuer Breakdown */}
      <div className="card mb-8">
        <div className="card-header">
          <h2 className="text-xl font-semibold">Issuer Breakdown</h2>
        </div>
        
        {Object.keys(stats.issuer_breakdown).length === 0 ? (
          <div className="text-center py-8">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No issuer data available</p>
          </div>
        ) : (
          <div className="space-y-4">
            {Object.entries(stats.issuer_breakdown)
              .sort(([,a], [,b]) => b - a)
              .map(([issuer, count]) => (
                <div key={issuer} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                    <span className="font-medium">{issuer.toUpperCase()}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-2xl font-bold text-blue-600">
                      {formatNumber(count)}
                    </span>
                    <span className="text-sm text-gray-600">
                      {formatPercentage(count / stats.total_statements)} of total
                    </span>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold">Processing Performance</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Success Rate</span>
              <div className="flex items-center gap-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full" 
                    style={{ 
                      width: `${(stats.processed_statements / Math.max(stats.total_statements, 1)) * 100}%` 
                    }}
                  ></div>
                </div>
                <span className="font-semibold">
                  {formatPercentage(stats.processed_statements / Math.max(stats.total_statements, 1))}
                </span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-600">Error Rate</span>
              <div className="flex items-center gap-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-red-600 h-2 rounded-full" 
                    style={{ 
                      width: `${(stats.error_statements / Math.max(stats.total_statements, 1)) * 100}%` 
                    }}
                  ></div>
                </div>
                <span className="font-semibold">
                  {formatPercentage(stats.error_statements / Math.max(stats.total_statements, 1))}
                </span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-600">Average Confidence</span>
              <div className="flex items-center gap-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-600 h-2 rounded-full" 
                    style={{ 
                      width: `${stats.average_confidence * 100}%` 
                    }}
                  ></div>
                </div>
                <span className="font-semibold">
                  {formatPercentage(stats.average_confidence)}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold">System Health</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <span className="font-medium">Processing Status</span>
              </div>
              <div className="badge badge-success">Healthy</div>
            </div>

            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <span className="font-medium">AI Provider</span>
              </div>
              <div className="badge badge-info">Active</div>
            </div>

            <div className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <Clock className="h-5 w-5 text-yellow-600" />
                <span className="font-medium">Last Updated</span>
              </div>
              <span className="text-sm text-gray-600">Just now</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card mt-8">
        <div className="card-header">
          <h2 className="text-xl font-semibold">Recommendations</h2>
        </div>
        
        <div className="space-y-3">
          {stats.average_confidence < 0.7 && (
            <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>Low Confidence:</strong> Consider improving PDF quality or using higher resolution scans for better extraction results.
              </p>
            </div>
          )}
          
          {stats.error_statements > stats.processed_statements * 0.1 && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-800">
                <strong>High Error Rate:</strong> Review failed extractions and consider updating extraction patterns for better accuracy.
              </p>
            </div>
          )}
          
          {stats.average_confidence >= 0.8 && stats.error_statements < stats.total_statements * 0.05 && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800">
                <strong>Excellent Performance:</strong> Your extraction system is performing well with high confidence and low error rates.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default StatsPage
