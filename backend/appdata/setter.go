package appdata

func (a *AppData) SetBool(key string, value bool) error {
	return a.set(key, value)
}

func (a *AppData) SetBoolSlice(key string, value []bool) error {
	return a.set(key, value)
}

func (a *AppData) SetFloat(key string, value float64) error {
	return a.set(key, value)
}

func (a *AppData) SetFloatSlice(key string, value []float64) error {
	return a.set(key, value)
}

func (a *AppData) SetInt(key string, value int) error {
	return a.set(key, value)
}

func (a *AppData) SetIntSlice(key string, value []int) error {
	return a.set(key, value)
}

func (a *AppData) SetString(key string, value string) error {
	return a.set(key, value)
}

func (a *AppData) SetStringSlice(key string, value []string) error {
	return a.set(key, value)
}
