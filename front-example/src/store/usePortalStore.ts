import { create } from 'zustand'

type UniversityUser = {
  email: string
  password: string
  universityName: string
}

type UploadedFileInfo = {
  name: string
  size: number
  type: string
  uploadedAt: string
}

type PortalState = {
  currentUser: Omit<UniversityUser, 'password'> | null
  lastUploadedFile: UploadedFileInfo | null
  loginError: string | null
  login: (email: string, password: string) => boolean
  logout: () => void
  registerUpload: (file: File) => void
  clearLoginError: () => void
}

const mockUsers: UniversityUser[] = [
  {
    email: 'admin@universidada.edu.co',
    password: 'demo123',
    universityName: 'Universidad A',
  },
  {
    email: 'admin@universidadb.edu.co',
    password: 'demo123',
    universityName: 'Universidad B',
  },
  {
    email: 'admin@universidadc.edu.co',
    password: 'demo123',
    universityName: 'Universidad C',
  },
]

export const usePortalStore = create<PortalState>((set) => ({
  currentUser: null,
  lastUploadedFile: null,
  loginError: null,
  login: (email, password) => {
    const user = mockUsers.find(
      (item) => item.email.toLowerCase() === email.toLowerCase() && item.password === password,
    )

    if (!user) {
      set({ loginError: 'Credenciales inválidas. Usa las credenciales de demo.', currentUser: null })
      return false
    }

    set({
      currentUser: { email: user.email, universityName: user.universityName },
      loginError: null,
    })
    return true
  },
  logout: () => set({ currentUser: null }),
  registerUpload: (file) =>
    set({
      lastUploadedFile: {
        name: file.name,
        size: file.size,
        type: file.type || 'application/octet-stream',
        uploadedAt: new Date().toISOString(),
      },
    }),
  clearLoginError: () => set({ loginError: null }),
}))
