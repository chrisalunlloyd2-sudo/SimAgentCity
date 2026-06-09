# TIMESTAMP: 2026-06-08T11:00:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-ToK

import mmap
import os
import struct

class ToKMemoryArena:
    """Phase 1: Native Memory Arena for Radix-Trie ToK."""
    def __init__(self, size_mb=128):
        self.size = size_mb * 1024 * 1024
        # Allocate flat memory space
        self.fd = os.open("tok_arena.bin", os.O_RDWR | os.O_CREAT | os.O_TRUNC)
        os.ftruncate(self.fd, self.size)
        self.arena = mmap.mmap(self.fd, self.size)
        
    def write_node(self, offset, uuid, parent_offset, child_ptr, weight, flags):
        """Writes a 64-byte dense node payload."""
        # UUID(8), Parent(2), Child(2), Weight(2), Flags(2) = 16 bytes. 
        # Padding to 64 bytes for cache alignment
        data = struct.pack('QHHHHH', uuid, parent_offset, child_ptr, weight, flags, 0)
        self.arena[offset:offset+16] = data
        
    def read_node(self, offset):
        return struct.unpack('QHHHHH', self.arena[offset:offset+16])
