# PicoBrain Modern UI Framework

## Overview
This framework provides a consistent, modern design system based on the Dashboard's v0 styling. It includes glass-morphism effects, gradient backgrounds, animations, and reusable components.

## Quick Start Guide

### 1. Theme Configuration
Located at: `/src/lib/theme.ts`

The theme file contains:
- Color palette (primary, secondary, gradients)
- Glass effect styles
- Animation configurations
- Common style presets

### 2. Styled Components
Located at: `/src/components/styled/index.tsx`

Available components:
- **StyledCard**: Glass-effect cards with animation
- **StyledTable**: Modern table with loading state
- **StyledButton**: Gradient buttons with hover effects
- **StyledInput**: Glass-effect input fields
- **PageHeader**: Animated page headers
- **StatsCard**: Dashboard-style stat cards
- **LoadingSpinner**: Modern loading indicator
- **StyledModal**: Glass-effect modals

### 3. Page Template
Located at: `/src/components/templates/PageTemplate.tsx`

Use this template for consistent page layouts.

## Converting Existing Pages

### Example: Converting the Persons Page

#### Before (Basic Style):
```tsx
export default function PersonsPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Persons Management</h1>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <button className="btn-primary">Add New Person</button>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table>...</table>
      </div>
    </div>
  );
}
```

#### After (Modern Style):
```tsx
import { PageTemplate } from '@/components/templates/PageTemplate';
import { StyledCard, StyledTable, StyledButton, StyledInput, StyledModal } from '@/components/styled';
import { Plus } from 'lucide-react';

export default function PersonsPage() {
  return (
    <PageTemplate
      title="Persons Management"
      description="Manage all persons in the system"
      actions={
        <StyledButton variant="primary" onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add New Person
        </StyledButton>
      }
    >
      {/* Search Bar */}
      <StyledCard className="mb-6">
        <div className="p-4">
          <StyledInput
            placeholder="Search by name, email, or phone..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </StyledCard>

      {/* Data Table */}
      <StyledTable
        headers={['Name', 'Email', 'Phone', 'Gender', 'Date of Birth']}
        data={transformedData}
        loading={isLoading}
        actions={(item) => (
          <>
            <StyledButton variant="ghost" onClick={() => handleEdit(item)}>
              Edit
            </StyledButton>
            <StyledButton variant="ghost" onClick={() => handleDelete(item.id)}>
              Delete
            </StyledButton>
          </>
        )}
      />

      {/* Modal */}
      <StyledModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Add New Person"
      >
        {/* Form content */}
      </StyledModal>
    </PageTemplate>
  );
}
```

## Global Styles Applied

The following styles are automatically applied:

### Body
- Gradient background: `from-gray-50 via-white to-cyan-50/20`
- Modern font rendering

### Buttons
- **Primary**: Cyan to blue gradient with hover effects
- **Secondary**: Glass effect with backdrop blur
- **Ghost**: Transparent with hover background

### Cards
- Glass morphism: `bg-white/80 backdrop-blur-md`
- Soft borders: `border-white/50`
- Hover shadow transitions

### Tables
- Glass effect wrapper
- Animated row entries
- Hover state highlighting

### Inputs
- Semi-transparent background
- Focus ring with cyan accent
- Smooth transitions

## Animation Guide

### Using Framer Motion

```tsx
import { motion } from 'framer-motion';

// Fade in animation
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>

// Hover effect
<motion.div whileHover={{ y: -4 }}>
  Hover me
</motion.div>

// Stagger children
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    visible: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }}
>
  {items.map(item => (
    <motion.div
      variants={{
        hidden: { opacity: 0, x: -20 },
        visible: { opacity: 1, x: 0 }
      }}
    >
      {item}
    </motion.div>
  ))}
</motion.div>
```

## CSS Classes Available

### Layout
- `page-background`: Full gradient background
- `card`: Glass effect card
- `card-glass`: Glass effect only
- `table-container`: Modern table wrapper

### Typography
- `gradient-text`: Gradient text effect
- Standard Tailwind typography classes

### Effects
- `glass-effect`: Apply glass morphism
- `shadow-glow`: Cyan glow shadow
- `hover-lift`: Lift on hover
- `hover-grow`: Scale on hover
- `pulse-glow`: Pulsing animation

### Status
- `status-dot`: Base status indicator
- `status-dot-active`: Green dot
- `status-dot-warning`: Yellow dot
- `status-dot-error`: Red dot

## Color Palette

### Primary (Cyan)
- `cyan-50` to `cyan-900`
- Primary: `cyan-500` (#06b6d4)
- Hover: `cyan-600` (#0891b2)

### Secondary (Blue)
- `blue-400` to `blue-600`
- Secondary: `blue-500` (#3b82f6)
- Hover: `blue-600` (#2563eb)

### Gradients
- Primary: `from-cyan-500 to-blue-500`
- Hover: `from-cyan-600 to-blue-600`
- Background: `from-gray-50 via-white to-cyan-50/20`

## Best Practices

1. **Always use the PageTemplate** for new pages to ensure consistency
2. **Import theme configuration** when you need custom styles
3. **Use StyledComponents** instead of basic HTML elements
4. **Add animations** for better user experience
5. **Maintain glass effect** consistency across components
6. **Use gradient buttons** for primary actions
7. **Apply hover states** to interactive elements

## Migration Checklist

When updating an existing page:

- [ ] Replace basic divs with PageTemplate
- [ ] Convert buttons to StyledButton
- [ ] Convert inputs to StyledInput
- [ ] Replace tables with StyledTable
- [ ] Convert modals to StyledModal
- [ ] Add Framer Motion animations
- [ ] Apply glass effects to cards
- [ ] Update color scheme to use cyan/blue
- [ ] Add loading states with modern spinner
- [ ] Test responsive behavior

## Component Examples

### Stats Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {stats.map((stat, index) => (
    <StatsCard
      key={stat.title}
      title={stat.title}
      value={stat.value}
      change={stat.change}
      trend={stat.trend}
      icon={stat.icon}
    />
  ))}
</div>
```

### Search Bar with Glass Effect
```tsx
<StyledCard className="mb-6">
  <div className="flex gap-4 p-4">
    <StyledInput
      placeholder="Search..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="flex-1"
    />
    <StyledButton variant="primary">
      Search
    </StyledButton>
  </div>
</StyledCard>
```

### Action Buttons Group
```tsx
<div className="flex gap-2">
  <StyledButton variant="primary">
    <Plus className="w-4 h-4 mr-2" />
    Add New
  </StyledButton>
  <StyledButton variant="secondary">
    <Download className="w-4 h-4 mr-2" />
    Export
  </StyledButton>
  <StyledButton variant="ghost">
    <Filter className="w-4 h-4 mr-2" />
    Filter
  </StyledButton>
</div>
```

## Notes

- The framework is designed to be progressively adopted
- You can mix old and new styles during migration
- All components support TypeScript
- Glass effects degrade gracefully in older browsers
- Animations can be disabled for accessibility

## Future Enhancements

- [ ] Dark mode support
- [ ] More animation presets
- [ ] Additional component variations
- [ ] Form validation styles
- [ ] Chart styling templates
- [ ] Notification system styling