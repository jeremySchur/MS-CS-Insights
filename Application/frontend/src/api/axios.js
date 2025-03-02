import axios from 'axios';
const BASE_URL = import.meta.env.VITE_BACKEND_API_URL;

export default axios.create({
    baseURL: BASE_URL
});
