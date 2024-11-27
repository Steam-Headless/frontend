import axios from 'axios';

class ConfigService {
    constructor() {
        this.config = null;
    }

    async serverConfig() {
        // If config is already loaded, return it
        if (this.config) {
            return this.config;
        }

        try {
            // Fetch the config from the backend
            const response = await axios.get('/api/config');
            this.config = response.data; // Cache the config
            return this.config;
        } catch (error) {
            console.error('Error fetching configuration:', error);
            throw new Error('Failed to fetch configuration');
        }
    }
}

// Export a singleton instance of ConfigService
const configService = new ConfigService();
export default configService;
