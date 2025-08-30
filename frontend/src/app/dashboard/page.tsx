"use client"

import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Users,
  Calendar,
  Activity,
  TrendingUp,
  TrendingDown,
  Search,
  Bell,
  Settings,
  Menu,
  Plus,
  Download,
  Filter,
  MoreHorizontal,
  Edit,
  Trash2,
  Eye,
  ChevronLeft,
  ChevronRight,
  Moon,
  Sun,
  Heart,
  Stethoscope,
  Pill,
  FileText,
  Clock,
  Building2,
  UserCheck,
  Briefcase,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { personService, clinicService, clientService, employeeService } from '@/services/api.service'

// Chart data configurations
const chartData = {
  registrations: [
    { month: "Jan", patients: 245, staff: 12 },
    { month: "Feb", patients: 289, staff: 15 },
    { month: "Mar", patients: 312, staff: 18 },
    { month: "Apr", patients: 278, staff: 14 },
    { month: "May", patients: 334, staff: 20 },
    { month: "Jun", patients: 356, staff: 22 },
    { month: "Jul", patients: 398, staff: 25 },
    { month: "Aug", patients: 423, staff: 28 },
    { month: "Sep", patients: 445, staff: 30 },
    { month: "Oct", patients: 467, staff: 32 },
    { month: "Nov", patients: 489, staff: 35 },
    { month: "Dec", patients: 512, staff: 38 },
  ],
  clinics: [
    { name: "Main Clinic", value: 45, color: "#0ea5e9" },
    { name: "North Branch", value: 25, color: "#0c4a6e" },
    { name: "South Branch", value: 20, color: "#fbbf24" },
    { name: "East Branch", value: 10, color: "#f472b6" },
  ],
  staff: [
    { department: "Doctors", count: 24 },
    { department: "Nurses", count: 45 },
    { department: "Admin", count: 12 },
    { department: "Support", count: 18 },
  ],
  revenue: [
    { month: "Jan", revenue: 65000, expenses: 45000 },
    { month: "Feb", revenue: 72000, expenses: 48000 },
    { month: "Mar", revenue: 68000, expenses: 46000 },
    { month: "Apr", revenue: 75000, expenses: 49000 },
    { month: "May", revenue: 82000, expenses: 52000 },
    { month: "Jun", revenue: 89000, expenses: 55000 },
  ],
}

const sidebarItems = [
  { icon: Activity, label: "Dashboard", active: true, badge: null },
  { icon: Users, label: "Persons", active: false, badge: null, link: "/dashboard/persons" },
  { icon: Building2, label: "Clinics", active: false, badge: null },
  { icon: UserCheck, label: "Clients", active: false, badge: null },
  { icon: Briefcase, label: "Employees", active: false, badge: null },
  { icon: Calendar, label: "Appointments", active: false, badge: "12" },
  { icon: FileText, label: "Medical Records", active: false, badge: null },
  { icon: Heart, label: "Emergency", active: false, badge: "3" },
  { icon: Settings, label: "Settings", active: false, badge: null },
]

export default function HealthcareDashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [darkMode, setDarkMode] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const [currentPage, setCurrentPage] = useState(1)
  const [showAddPatient, setShowAddPatient] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  
  // Real data from backend
  const [stats, setStats] = useState({
    totalPersons: 0,
    totalClinics: 0,
    totalClients: 0,
    totalEmployees: 0,
    personChange: 0,
    clinicChange: 0,
    clientChange: 0,
    employeeChange: 0,
  })
  
  const [recentActivity, setRecentActivity] = useState<any[]>([])
  const [persons, setPersons] = useState<any[]>([])

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setIsLoading(true)
      
      // Fetch data from all services
      const results = await Promise.allSettled([
        personService.getAll({ page_size: 5 }),
        clinicService.getAll({ page_size: 1 }),
        clientService.getAll({ page_size: 1 }),
        employeeService.getAll({ page_size: 1 }),
      ])

      // Extract data with error handling
      const personsData = results[0].status === 'fulfilled' ? results[0].value : { items: [], total: 0 }
      const clinicsData = results[1].status === 'fulfilled' ? results[1].value : { total: 0 }
      const clientsData = results[2].status === 'fulfilled' ? results[2].value : { total: 0 }
      const employeesData = results[3].status === 'fulfilled' ? results[3].value : { total: 0 }

      setStats({
        totalPersons: personsData.total || 0,
        totalClinics: clinicsData.total || 0,
        totalClients: clientsData.total || 0,
        totalEmployees: employeesData.total || 0,
        personChange: 12.5, // These would come from backend comparison
        clinicChange: 3.2,
        clientChange: 8.1,
        employeeChange: 15.3,
      })
      
      setPersons(personsData.items || [])
      
      // Sample recent activity (would come from backend)
      setRecentActivity([
        { id: 1, description: 'New patient registered: Jane Smith', time: '2 minutes ago', type: 'patient' },
        { id: 2, description: 'Appointment scheduled for John Doe', time: '15 minutes ago', type: 'appointment' },
        { id: 3, description: 'Dr. Wilson updated availability', time: '1 hour ago', type: 'staff' },
        { id: 4, description: 'Lab results uploaded for Patient #1234', time: '2 hours ago', type: 'medical' },
        { id: 5, description: 'New employee onboarded: Sarah Johnson', time: '3 hours ago', type: 'staff' },
      ])
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const statsData = [
    { title: "Total Persons", value: stats.totalPersons, change: stats.personChange, trend: stats.personChange > 0 ? "up" : "down", icon: Users },
    { title: "Active Clinics", value: stats.totalClinics, change: stats.clinicChange, trend: stats.clinicChange > 0 ? "up" : "down", icon: Building2 },
    { title: "Total Clients", value: stats.totalClients, change: stats.clientChange, trend: stats.clientChange > 0 ? "up" : "down", icon: UserCheck },
    { title: "Employees", value: stats.totalEmployees, change: stats.employeeChange, trend: stats.employeeChange > 0 ? "up" : "down", icon: Briefcase },
  ]

  const AnimatedCounter = ({ value, prefix = "" }: { value: number; prefix?: string }) => {
    return (
      <motion.span
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-2xl font-bold"
      >
        {prefix}
        {value.toLocaleString()}
      </motion.span>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-gray-50 via-white to-cyan-50/20">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-cyan-200 border-t-cyan-500 rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <Activity className="w-6 h-6 text-cyan-500" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br from-gray-50 via-white to-cyan-50/20 ${darkMode ? "dark" : ""}`}>
      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: sidebarOpen ? 280 : 80 }}
        className="fixed left-0 top-0 h-full bg-white/95 backdrop-blur-md border-r border-gray-200 z-40"
      >
        <div className="p-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-cyan-500 rounded-lg flex items-center justify-center">
              <Stethoscope className="w-5 h-5 text-white" />
            </div>
            <AnimatePresence>
              {sidebarOpen && (
                <motion.h1
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="text-xl font-bold text-gray-900"
                >
                  PicoBrain Pro
                </motion.h1>
              )}
            </AnimatePresence>
          </div>
        </div>

        <nav className="px-4 space-y-2">
          {sidebarItems.map((item, index) => (
            <motion.div
              key={item.label}
              whileHover={{ x: 4 }}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                item.active
                  ? "bg-cyan-50 text-cyan-700"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              }`}
              onClick={() => {
                if (item.link && window.location.pathname !== item.link) {
                  window.location.href = item.link
                }
              }}
            >
              <item.icon className="w-5 h-5" />
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.span
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="flex-1"
                  >
                    {item.label}
                  </motion.span>
                )}
              </AnimatePresence>
              {item.badge && sidebarOpen && (
                <Badge variant="secondary" className="text-xs">
                  {item.badge === "dynamic" ? stats.totalPersons : item.badge}
                </Badge>
              )}
            </motion.div>
          ))}
        </nav>

        <div className="absolute bottom-6 left-4 right-4">
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-100/50">
            <Avatar className="w-8 h-8">
              <AvatarImage src="/caring-doctor.png" />
              <AvatarFallback>DR</AvatarFallback>
            </Avatar>
            <AnimatePresence>
              {sidebarOpen && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="flex-1"
                >
                  <p className="text-sm font-medium text-gray-900">Dr. Smith</p>
                  <p className="text-xs text-gray-600">Administrator</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? "ml-[280px]" : "ml-[80px]"}`}>
        {/* Header */}
        <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-30">
          <div className="flex items-center justify-between p-6">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" onClick={() => setSidebarOpen(!sidebarOpen)}>
                <Menu className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600">Welcome to PicoBrain Healthcare System</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="Search patients, appointments..."
                  className="pl-10 w-80 bg-white/50 backdrop-blur-sm"
                />
              </div>

              <Button variant="ghost" size="sm">
                <Bell className="w-5 h-5" />
              </Button>

              <Button variant="ghost" size="sm" onClick={() => setDarkMode(!darkMode)}>
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </Button>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6 space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {statsData.map((stat, index) => (
              <motion.div
                key={stat.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -4 }}
              >
                <Card className="bg-white/80 backdrop-blur-md border-white/50 hover:shadow-lg transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-600 text-sm">{stat.title}</p>
                        <AnimatedCounter value={stat.value} prefix={stat.prefix} />
                        <div className="flex items-center gap-1 mt-2">
                          {stat.trend === "up" ? (
                            <TrendingUp className="w-4 h-4 text-green-500" />
                          ) : (
                            <TrendingDown className="w-4 h-4 text-red-500" />
                          )}
                          <span className={`text-sm ${stat.trend === "up" ? "text-green-500" : "text-red-500"}`}>
                            {Math.abs(stat.change)}%
                          </span>
                        </div>
                      </div>
                      <div className="w-12 h-12 bg-cyan-50 rounded-lg flex items-center justify-center">
                        <stat.icon className="w-6 h-6 text-cyan-500" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Patient Registrations Chart */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle>Patient Registrations</CardTitle>
                <CardDescription>Monthly patient registration trends</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData.registrations}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="month" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.95)",
                        backdropFilter: "blur(10px)",
                        border: "1px solid rgba(229, 231, 235, 0.5)",
                        borderRadius: "8px",
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="patients"
                      stroke="#0ea5e9"
                      strokeWidth={3}
                      dot={{ fill: "#0ea5e9", r: 4 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="staff"
                      stroke="#10b981"
                      strokeWidth={3}
                      dot={{ fill: "#10b981", r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Clinic Distribution */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle>Clinic Distribution</CardTitle>
                <CardDescription>Patient distribution across clinics</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={chartData.clinics}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={120}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {chartData.clinics.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Staff by Department */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle>Staff by Department</CardTitle>
                <CardDescription>Current staff distribution</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData.staff}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="department" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.95)",
                        backdropFilter: "blur(10px)",
                        border: "1px solid rgba(229, 231, 235, 0.5)",
                        borderRadius: "8px",
                      }}
                    />
                    <Bar dataKey="count" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Revenue Trends */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle>Revenue Trends</CardTitle>
                <CardDescription>Monthly revenue performance</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={chartData.revenue}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="month" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.95)",
                        backdropFilter: "blur(10px)",
                        border: "1px solid rgba(229, 231, 235, 0.5)",
                        borderRadius: "8px",
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="revenue"
                      stroke="#0ea5e9"
                      fill="rgba(14, 165, 233, 0.2)"
                      strokeWidth={2}
                    />
                    <Area
                      type="monotone"
                      dataKey="expenses"
                      stroke="#ef4444"
                      fill="rgba(239, 68, 68, 0.2)"
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions & Widgets */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recent Activity */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentActivity.map((activity) => (
                  <div
                    key={activity.id}
                    className="flex items-center gap-3 p-3 bg-gray-50/50 rounded-lg hover:bg-gray-100/50 transition-colors"
                  >
                    <div className={`w-2 h-2 rounded-full animate-pulse ${
                      activity.type === 'patient' ? 'bg-blue-500' :
                      activity.type === 'appointment' ? 'bg-green-500' :
                      activity.type === 'staff' ? 'bg-purple-500' :
                      'bg-orange-500'
                    }`} />
                    <div className="flex-1">
                      <p className="text-sm text-gray-900">{activity.description}</p>
                      <p className="text-xs text-gray-500">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Emergency Contacts */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="w-5 h-5 text-red-500" />
                  Emergency Contacts
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  { name: "Emergency Room", number: "+1 (555) 911-0000", status: "Available" },
                  { name: "On-Call Doctor", number: "+1 (555) 123-4567", status: "Available" },
                  { name: "Pharmacy", number: "+1 (555) 987-6543", status: "Closed" },
                ].map((contact, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50/50 rounded-lg">
                    <div>
                      <p className="font-medium">{contact.name}</p>
                      <p className="text-sm text-gray-600">{contact.number}</p>
                    </div>
                    <Badge variant={contact.status === "Available" ? "default" : "secondary"}>{contact.status}</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card className="bg-white/80 backdrop-blur-md border-white/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600"
                  onClick={() => window.location.href = '/dashboard/persons'}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add New Person
                </Button>
                <Button variant="outline" className="w-full">
                  <Calendar className="w-4 h-4 mr-2" />
                  Schedule Appointment
                </Button>
                <Button variant="outline" className="w-full">
                  <FileText className="w-4 h-4 mr-2" />
                  Generate Report
                </Button>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>

      {/* Floating Action Button */}
      <motion.div 
        className="fixed bottom-6 right-6 z-50" 
        whileHover={{ scale: 1.1 }} 
        whileTap={{ scale: 0.9 }}
      >
        <Button
          size="lg"
          className="rounded-full w-14 h-14 shadow-lg bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600"
          onClick={() => setShowAddPatient(true)}
        >
          <Plus className="w-6 h-6" />
        </Button>
      </motion.div>

      {/* Add Patient Dialog */}
      <Dialog open={showAddPatient} onOpenChange={setShowAddPatient}>
        <DialogContent className="bg-white/95 backdrop-blur-md">
          <DialogHeader>
            <DialogTitle>Add New Patient</DialogTitle>
            <DialogDescription>Enter patient information to create a new record</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="firstName">First Name</Label>
                <Input id="firstName" placeholder="Enter first name" />
              </div>
              <div>
                <Label htmlFor="lastName">Last Name</Label>
                <Input id="lastName" placeholder="Enter last name" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="age">Age</Label>
                <Input id="age" type="number" placeholder="Enter age" />
              </div>
              <div>
                <Label htmlFor="gender">Gender</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select gender" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label htmlFor="condition">Primary Condition</Label>
              <Input id="condition" placeholder="Enter primary condition" />
            </div>
            <div>
              <Label htmlFor="notes">Notes</Label>
              <Textarea id="notes" placeholder="Additional notes..." />
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setShowAddPatient(false)}>
                Cancel
              </Button>
              <Button 
                className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600"
                onClick={() => setShowAddPatient(false)}
              >
                Add Patient
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
