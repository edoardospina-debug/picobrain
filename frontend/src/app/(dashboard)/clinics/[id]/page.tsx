'use client';

import ClinicForm from '@/components/features/clinics/ClinicForm';

interface EditClinicPageProps {
  params: {
    id: string;
  };
}

export default function EditClinicPage({ params }: EditClinicPageProps) {
  return <ClinicForm mode="edit" clinicId={params.id} />;
}
