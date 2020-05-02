proj=async-ex

LIBFLAGS += -pthread

$(proj): $(proj).o
	$(CXX) $(CXXFLAGS) $(LIBFLAGS) $< -o $@

$(proj).o: $(proj).cpp
	$(CXX) -std=c++11 -c $< -o $@

.PHONY = clean

clean:
	rm -rf $(proj).o $(proj)
