// --- Generic API Response Wrappers ---

export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
  message?: string;
}

export interface ApiErrorDetail {
  field?: string;
  message: string;
  code: string;
}

export interface ApiErrorResponse {
  success: false;
  error: ApiErrorDetail;
}

// A type guard to easily differentiate between success and error responses
export function isApiErrorResponse(response: unknown): response is ApiErrorResponse {
  if (typeof response !== 'object' || response === null) {
    return false;
  }
  const res = response as { success?: unknown; error?: unknown };
  return res.success === false && res.error !== undefined;
}

export interface PaginationMetadata {
  page: number;
  per_page: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationMetadata;
}
