import axios from 'axios';

export const getScenes = () => {
  return axios.get('/api/scenes');
};
