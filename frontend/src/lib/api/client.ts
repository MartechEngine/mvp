import axios, { AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { getAuthToken, getRefreshToken, setAuthTokens, clearAuthTokens } from '@/lib/utils/auth-storage';
import { ApiErrorResponse, ApiSuccessResponse } from '@/types/api';
import { TokenResponse } from '@/types/auth';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Track if we're currently refreshing to prevent multiple refresh attempts
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value: string | null) => void;
  reject: (error: AxiosError) => void;
}> = [];

// Process the queue of failed requests after token refresh
const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  
  failedQueue = [];
};

// --- Request Interceptor ---
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    config.headers['X-Device-ID'] = localStorage.getItem('device_id') || generateDeviceId();
    config.headers['X-Device-Name'] = getDeviceName();
    config.headers['X-Device-Type'] = getDeviceType();
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- Response Interceptor with Token Refresh ---
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${token}`;
          }
          return apiClient(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }
      
      originalRequest._retry = true;
      isRefreshing = true;
      
      const refreshToken = getRefreshToken();
      
      if (!refreshToken) {
        clearAuthTokens();
        window.location.href = '/auth/login';
        return Promise.reject(error);
      }
      
      try {
        const response = await axios.post<ApiSuccessResponse<TokenResponse>>(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/refresh`,
          { refresh_token: refreshToken },
          {
            headers: {
              'Content-Type': 'application/json',
              'X-Device-ID': localStorage.getItem('device_id') || generateDeviceId(),
              'X-Device-Name': getDeviceName(),
              'X-Device-Type': getDeviceType(),
            }
          }
        );
        
        const { access_token, refresh_token: newRefreshToken, token_type } = response.data.data;
        
        setAuthTokens({ access_token, refresh_token: newRefreshToken, token_type });
        
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }
        
        processQueue(null, access_token);
        
        return apiClient(originalRequest);
        
      } catch (refreshError) {
        processQueue(axios.isAxiosError(refreshError) ? refreshError : new AxiosError('Token refresh failed'), null);
        clearAuthTokens();
        
        if (window.location.pathname !== '/auth/login') {
          window.location.href = '/auth/login';
        }
        
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    
    const apiError = error.response?.data as ApiErrorResponse;

    if (apiError && apiError.error) {
      return Promise.reject(new Error(apiError.error.message));
    }

    return Promise.reject(new Error(error.message || 'An unexpected network error occurred.'));
  }
);

// --- Device Information Utilities ---
function generateDeviceId(): string {
  const deviceId = 'device_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
  localStorage.setItem('device_id', deviceId);
  return deviceId;
}

function getDeviceName(): string {
  const userAgent = navigator.userAgent;
  
  if (/iPhone/.test(userAgent)) return 'iPhone';
  if (/iPad/.test(userAgent)) return 'iPad';
  if (/Android/.test(userAgent)) return 'Android Device';
  if (/Mac/.test(userAgent)) return 'Mac';
  if (/Windows/.test(userAgent)) return 'Windows PC';
  if (/Linux/.test(userAgent)) return 'Linux PC';
  
  return 'Unknown Device';
}

function getDeviceType(): string {
  const userAgent = navigator.userAgent;
  
  if (/Mobile|Android|iPhone/.test(userAgent)) return 'mobile';
  if (/iPad|Tablet/.test(userAgent)) return 'tablet';
  
  return 'desktop';
}

export { apiClient };
