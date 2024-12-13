import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';
import jwt_decode from 'jwt-decode';


@Injectable({
  providedIn: 'root',
})



export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000'; // FastAPI base URL
  user = {id:0, full_name: '', email: '' };

  private booleanSubject = new BehaviorSubject<boolean>(this.getBooleanValue());
  boolean$ = this.booleanSubject.asObservable();
   // Method to update the boolean value
   setBooleanValue(value: boolean): void {
    
    this.booleanSubject.next(value);
    localStorage.setItem('isLoggedIn', JSON.stringify(value));
  }

  // Method to get the current boolean value
  getBooleanValue(): boolean {
    const storedState = localStorage.getItem('isLoggedIn');
    return storedState ? JSON.parse(storedState) : false;
  }
  setUser(User:{id:number,full_name: string, email: string; }){
    this.user=User;
  }
  getUser(){
      return this.user;
  }
  constructor(private http: HttpClient) {}

  registerUser(userData: {full_name: string, email: string; password: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/register`, userData);
  }
  loginUser(userData: {email: string; password: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, userData);
  }

  isLoggedIn(): boolean {
    const userToken = localStorage.getItem('userToken');
    return !!userToken; // Return true if the token exists
}

decodeToken(token: string) {
  try {
    const decodedToken = jwt_decode(token);
    console.log(decodedToken);  // Log the decoded token
    return decodedToken;        // Return the decoded token data
  } catch (error) {
    console.error('Invalid token:', error);
    return null;
  }
}



}
