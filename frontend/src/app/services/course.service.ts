import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams, HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class CourseService {
  private apiUrl = 'http://127.0.0.1:8000'; // Replace with your FastAPI backend URL

  constructor(private http: HttpClient) {}

  sendMessage(course_id:number,sender: string, text: string): Observable<any> {
    return this.http.post(this.apiUrl+"/chat/", {course_id, sender, text });
  }

  getChatHistory(course_id:number): Observable<any> {
    return this.http.get(`${this.apiUrl}/chat/history/${course_id}/`);
  }

  uploadCourse(name: string, userId: number, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('user_id', userId.toString());
    formData.append('file', file);

    const headers = new HttpHeaders();

    return this.http.post(this.apiUrl+"/upload_course/", formData, { headers: headers }).pipe(
      catchError((error) => {
        console.error('Error uploading course:', error);
        throw error; // Handle the error appropriately
      })
    );
  }
  getCoursesByUser(): Observable<any> {
    const token = localStorage.getItem('userToken'); // Get token from localStorage or sessionStorage

    // Check if token exists
    if (!token) {
      throw new Error('User is not authenticated');
    }
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    // Make GET request to backend API
    return this.http.get(this.apiUrl+"/courses/", { headers });;
  }
}
