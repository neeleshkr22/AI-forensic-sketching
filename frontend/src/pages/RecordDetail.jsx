import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, User, Calendar, MapPin, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import { recordsAPI } from '../services/api'

export default function RecordDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadRecord()
  }, [id])

  const loadRecord = async () => {
    try {
      const result = await recordsAPI.getById(id)
      setRecord(result.record)
    } catch (error) {
      toast.error('Failed to load record')
      navigate('/records')
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="loading-spinner" />
      </div>
    )
  }

  if (!record) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-600">Record not found</p>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto">
      <button
        onClick={() => navigate('/records')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Records</span>
      </button>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Photo */}
        <div className="md:col-span-1">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="aspect-square bg-gray-100 rounded-lg mb-4 overflow-hidden">
              {record.photo_url ? (
                <img
                  src={recordsAPI.getPhoto(record.record_id)}
                  alt={record.name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <User className="w-24 h-24 text-gray-300" />
                </div>
              )}
            </div>
            <div className="text-center">
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                record.status === 'active' ? 'bg-red-100 text-red-800' :
                record.status === 'caught' ? 'bg-green-100 text-green-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {record.status?.toUpperCase()}
              </span>
            </div>
          </div>
        </div>

        {/* Details */}
        <div className="md:col-span-2 space-y-6">
          {/* Basic Info */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">
              {record.name}
            </h1>

            <div className="grid md:grid-cols-2 gap-4">
              <InfoItem label="Record ID" value={record.record_id} />
              <InfoItem label="Age" value={record.age} />
              <InfoItem label="Gender" value={record.gender} />
              <InfoItem label="Height" value={record.height && `${record.height} cm`} />
              <InfoItem label="Weight" value={record.weight && `${record.weight} kg`} />
              <InfoItem label="Eye Color" value={record.eye_color} />
              <InfoItem label="Hair Color" value={record.hair_color} />
            </div>
          </div>

          {/* Crime Info */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center space-x-2">
              <AlertCircle className="w-6 h-6 text-red-600" />
              <span>Crime Information</span>
            </h2>

            <div className="space-y-3">
              <InfoItem label="Crime Type" value={record.crime_type} />
              <InfoItem label="Location" value={record.location} icon={MapPin} />
              <InfoItem 
                label="Date" 
                value={record.crime_date && new Date(record.crime_date).toLocaleDateString()} 
                icon={Calendar}
              />
              {record.description && (
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Description</p>
                  <p className="text-gray-800">{record.description}</p>
                </div>
              )}
            </div>
          </div>

          {/* Additional Details */}
          {(record.aliases?.length > 0 || record.tattoos?.length > 0 || record.scars?.length > 0) && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">
                Additional Details
              </h2>

              <div className="space-y-3">
                {record.aliases?.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Aliases</p>
                    <p className="text-gray-800">{record.aliases.join(', ')}</p>
                  </div>
                )}
                {record.tattoos?.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Tattoos</p>
                    <p className="text-gray-800">{record.tattoos.join(', ')}</p>
                  </div>
                )}
                {record.scars?.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Scars</p>
                    <p className="text-gray-800">{record.scars.join(', ')}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function InfoItem({ label, value, icon: Icon }) {
  if (!value) return null

  return (
    <div>
      <p className="text-sm font-medium text-gray-600 mb-1 flex items-center space-x-1">
        {Icon && <Icon className="w-4 h-4" />}
        <span>{label}</span>
      </p>
      <p className="text-gray-800">{value}</p>
    </div>
  )
}
