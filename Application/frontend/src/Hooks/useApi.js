import axios from '../api/axios';

const useApi = () => {
    const getChannels = async () => {
        const response = await axios.get('/');
        return response.data;
    };

    return { getChannels };
};

export default useApi;