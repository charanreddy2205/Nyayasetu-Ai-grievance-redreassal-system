// Convenience re-export of AuthContext hooks
// Separating hooks from the Provider component fixes the react/only-export-components lint rule
export { useAuth, useUser, useApiFetch } from './AuthContext';
